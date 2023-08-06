"""
This package is simple client to interact with Sonic 
via its socket protocol
Please note that it is still under development
"""
from __future__ import annotations

import socket
import logging
from enum import Enum
from typing import List


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pysonic')


class Mode(str, Enum):
    SEARCH = 'search'
    INGEST = 'ingest'


class Connection:
    """
    TCP socket wrapper
    """
    def __init__(self, socket):
        self._socket = socket
        self._reader = self._socket.makefile('rb', 0)
        self._writer = self._socket.makefile('wb', 0)

    @classmethod
    def open_connection(cls, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.settimeout(10)
        s.connect((ip, port))
        buf = s.recv(1024)
        if b'CONNECTED' in buf:
            logger.debug(f"{s} connected.")
            return cls(s)

    @property
    def reader(self):
        return self._reader

    @property
    def writer(self):
        return self._writer

    def close(self):
        return self._socket.close()


class Pool:
    """
    Pool to manage socket connections
    """
    def __init__(self, ip, port, size=10):
        self.size = size
        self.conn_in_used = set()
        self.pool = []
        for i in range(size):
            conn = Connection.open_connection(ip, port)
            self.pool.append(conn)

    def get_connection(self):
        for conn in self.pool:
            if conn not in self.conn_in_used:
                self.conn_in_used.add(conn)
                logger.debug(f"Obtained connection {conn}")
                return conn

    def release(self, conn):
        self.conn_in_used.remove(conn)
        logger.debug(f"{conn} released.")


class Client:
    """
    API to communicate with Sonic db
    """

    def __init__(self, 
            host: str = '127.0.0.1', 
            port: int = 1491, 
            password: str = 'SecretPassword',
            size=10,):
        self.host = host
        self.port = port
        self.password = password

        self.conn = None
        self._pool = Pool(host, port, size)

    def __enter__(self):
        self.conn = self._pool.get_connection()

    def __exit__(self, *args):
        self.conn.writer.write(b'QUIT\n')
        self._pool.release(self.conn)

    def ping(self):
        self.conn.writer.write(b'PING\n')
        return self.conn.reader.readline()

    def mode(self, mode: Mode):
        """

        TODO: read buffer value to breakdown command
        """
        self.conn.writer.write(bytes(f'START {mode} {self.password}\n', 'utf-8'))
        while True:
            line = self.conn.reader.readline()
            if bytes(f'STARTED {mode}', 'utf-8') in line:
                logger.info(f'Connected to Sonic with mode {mode}')
                return True

    def query(self, collection: str, bucket: str, terms: str, limit=10, offset=0):
        cmd = bytes(f'QUERY {collection} {bucket} "{terms}"\n', 'utf-8')
        self.conn.writer.write(cmd)
        event_id = None
        while True:
            line = self.conn.reader.readline()
            if b'PENDING' in line:
                event_id = self._parse_event_id(line)
                logger.info(f'Waiting for event {event_id}')
            elif event_id and event_id in line:
                return self._parse_query_results(line)

    def push(self, collection: str, bucket: str, object: str, text: str) -> bool:
        cmd = bytes(f'PUSH {collection} {bucket} {object} "{text}"\n', 'utf-8')
        self.conn.writer.write(cmd)
        while True:
            try:
                line = self.conn.reader.readline()
                if b'OK' in line:
                    return True
            except Exception as e:
                logger.exception(e)
                return False

    def suggest(self, collection: str, bucket: str, word: str, limit=10):
        cmd = bytes(f'SUGGEST {collection} {bucket} "{word}" LIMIT({limit})\n', 'utf-8')
        self.conn.writer.write(cmd)
        event_id = None
        while True:
            line = self.conn.reader.readline()
            if b'PENDING' in line:
                event_id = self._parse_event_id(line)
                logger.info(f'Waiting for event {event_id}')
            elif event_id and event_id in line:
                return self._parse_query_results(line)

    @staticmethod
    def _parse_event_id(line: bytes):
        id_ = line.split(b' ')[1]
        return id_.replace(b'\n', b'').replace(b'\r', b'')


    @staticmethod
    def _parse_query_results(line: bytes) -> List[str]:
        parts = line.replace(b'\n', b'').replace(b'\r', b'').split(b' ')
        results = parts[3:]
        return [r.decode('utf-8') for r in results]

