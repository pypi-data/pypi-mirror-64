import paramiko
from paramiko import SSHClient, AuthenticationException, SSHException
from multissh.utils import print_success, print_error, get_hostname, print_str, parse_response
import time


class Connection:
    __hostname = None
    __host = None
    __port = None
    __username = None
    __password = None

    __connection = None

    def __init__(self, host=None, port=None, username=None, password=None):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password

    def connect(self, max_tries=5, timeout=3):
        tries = 0

        while tries < max_tries:
            try:
                self.__connection = SSHClient()
                self.__connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.__connection.connect(hostname=self.__host, port=int(self.__port), username=self.__username, password=self.__password)

                if self.__connection.get_transport().is_active():
                    stdin, stdout, stderr = self.exec('hostname')

                    self.__hostname = get_hostname(('\n'.join(stdout)).strip())

                    print_success('Successfully connected!', self.__hostname)
                    return True
                else:
                    print_error('Connection failed!', self.__host)
                    return False

            except AuthenticationException:
                print_error('Authentication error!', self.__host)
                return False

            except SSHException as e:
                print_error(str(e), self.__host)
                return False

            except Exception as e:
                print_error('Connection failed with exception: %s' % str(e), self.__host)
                time.sleep(timeout * 1000)
                tries += 1

        return False

    def disconnect(self):
        self.exec('exit')
        self.__connection.close()

    def exec_cmd(self, command):
        stdin, stdout, stderr = self.exec(command)

        stderr = parse_response(stderr)
        stdout = parse_response(stdout)

        if stderr != "":
            print_error(stderr, self.__hostname)

        if stdout:
            print_str(stdout, 'info', self.__hostname)

    def exec(self, command, buffer_size=-1, timeout=10, get_pty=False, environment={}):
        if self.check_connection():
            return self.__connection.exec_command(command, bufsize=buffer_size, timeout=timeout, get_pty=get_pty, environment=environment)
        else:
            print_error('Unable to send command - connection closed!', self.__hostname)

        return False

    def check_connection(self):
        if not self.__connection.get_transport().is_active():
            print_error('Connection is closed, reconnecting...', self.__hostname)
            return self.connect()

        return True
