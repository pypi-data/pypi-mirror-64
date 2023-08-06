import os
import sys
from concurrent.futures.thread import ThreadPoolExecutor
import threading

import requests

from multissh.connection import Connection
from multissh.utils import parse_credentials, print_error, print_str, get_input


class MultiSSH:
    __running = True
    __verbose = False
    __source = None
    __workers = None
    __connections = []
    __thread_pool = []

    def __init__(self, config):
        self.__verbose = config['verbose']
        self.__source = config['source']
        self.__workers = config['workers']

    def run(self):
        credentials = []

        if self.__source.startswith('http://') or self.__source.startswith('https://'):
            try:
                response = requests.get(self.__source, headers={'User-agent': 'MultiSSH'})

                for line in response.text().split('\n'):
                    data = line.strip()

                    if data != "":
                        credentials.append(parse_credentials(data))

            except requests.exceptions.ConnectionError as e:
                print_error('Unable to download credentials: %s' % str(e))
            except Exception as e:
                print_error('Something went wrong: %s' % str(e))
        else:
            if os.path.exists(self.__source):
                with open(self.__source, 'r') as f:
                    for line in f.readlines():
                        data = line.strip()

                        if data != "":
                            credentials.append(parse_credentials(data))
            else:
                print_error('Credentials file: %s does not exist!' % self.__source)
                sys.exit(0)

        if len(credentials) == 0:
            print_error('There are no credentials')
            sys.exit(0)

        if not self.__workers:
            self.__workers = len(credentials)

        self.connect_to_hosts(credentials)

        timer = threading.Timer(60, self.health_check)
        timer.start()

        while self.__running:
            try:
                command = get_input()
            except KeyboardInterrupt:
                command = 'exit'

            if command == 'exit':
                self.__running = False
                self.disconnect_from_hosts()
            else:
                self.execute_cmd(command)

        print_str('\nBye bye!')
        sys.exit(0)

    def connect_to_hosts(self, credentials):
        for data in credentials:
            self.__connections.append(Connection(data['host'], data['port'], data['username'], data['password']))

        with ThreadPoolExecutor(max_workers=self.__workers) as executor:
            for connection in self.__connections:
                executor.submit(connection.connect)

    def disconnect_from_hosts(self):
        with ThreadPoolExecutor(max_workers=self.__workers) as executor:
            for connection in self.__connections:
                executor.submit(connection.disconnect)

    def execute_cmd(self, command):
        with ThreadPoolExecutor(max_workers=self.__workers) as executor:
            for connection in self.__connections:
                executor.submit(connection.exec_cmd, command)

    def health_check(self):
        with ThreadPoolExecutor(max_workers=self.__workers) as executor:
            for connection in self.__connections:
                executor.submit(connection.check_connection)

