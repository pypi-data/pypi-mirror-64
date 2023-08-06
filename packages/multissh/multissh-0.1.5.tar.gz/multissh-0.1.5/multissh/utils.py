from tldextract import tldextract


def get_hostname(hostname):
    h_data = tldextract.extract(hostname)

    if h_data.subdomain:
        hostname = h_data.subdomain
    else:
        if h_data.registered_domain:
            hostname = h_data.registered_domain

    return hostname


def print_str(message, str_type='info', hostname=None):
    if str_type == 'info':
        color = ConsoleColor.WHITE
    elif str_type == 'success':
        color = ConsoleColor.GREEN
    elif str_type == 'error':
        color = ConsoleColor.RED
    else:
        color = ConsoleColor.WHITE

    if hostname:
        print('%s[%s]: %s%s%s' % (ConsoleColor.HEADER, hostname, color, message, ConsoleColor.END))
    else:
        print('%s%s%s' % (color, message, ConsoleColor.END))


def print_error(message, hostname=None):
    print_str(message, 'error', hostname)


def print_success(message, hostname=None):
    print_str(message, 'success', hostname)


def parse_credentials(data):
    data = data.split(',')

    if len(data) != 4:
        print_error('Invalid credential line: %s' % ','.join(data))
        return False

    return {
        'host': data[0],
        'port': data[1],
        'username': data[2],
        'password': data[3]
    }


def parse_response(response):
    lines = []

    for line in response:
        line = line.strip()

        if line != '':
            lines.append(line)

    return '\n'.join(lines)


def get_input():
    return input('%s%s%s' % (ConsoleColor.GREEN, 'multissh$: ', ConsoleColor.END)).strip()


class ConsoleColor:
    GREEN = '\033[92m'
    RED = '\033[91m'
    HEADER = '\033[95m'
    END = '\033[0m'
    WHITE = '\33[37m'
