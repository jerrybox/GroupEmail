import imaplib
import configparser
import os
from pprint import pprint
import re


def open_connection(verbose=False):
    config = configparser.ConfigParser()
    config.read([os.path.expanduser('data.conf')])

    # Connect to the server.
    hostname = config.get('server', 'hostname')
    port = config.get('server', 'port')

    print('Connecting to', hostname)
    connection = imaplib.IMAP4_SSL(host=hostname, port=port)

    # Log in to our account.
    username = config.get('account', 'username')
    password = config.get('account', 'password')

    print('Logging in as', username)

    try:
        connection.login(username, password)
    except Exception as err:
        print(err)

    return connection


list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')


def parse_list_response(line):
    match = list_response_pattern.match(line.decode('utf-8'))
    flags, delimiter, mailbox_name = match.groups()
    mailbox_name = mailbox_name.strip('"')
    return flags, delimiter, mailbox_name


# with open_connection() as conn:
#     typ, data = conn.list()
#     print('Response code:', typ)

    # for line in data:
    #     print('Server response:', line)
    #     flags, delimiter, mailbox_name = parse_list_response(line)
    #     print('Parsed response:', (flags, delimiter, mailbox_name))

with open_connection() as conn:
    typ, data = conn.select('INBOX')
    result, data = conn.uid('search', None, '(SINCE "11-Nov-2019" BEFORE "13-Nov-2019")')
    print('Response code:', typ)
    uids = data[0].split()
    _, data2 = conn.uid('fetch', b','.join(uids), '(BODY[HEADER.FIELDS (MESSAGE-ID FROM TO CC DATE)])')
    pprint(data2)
    raw_file = open('raw-email-rec.csv', 'w')

    raw_file.write("Message-ID,Date,From,To,Cc\r\n")

    # Header for TSV file
    for line in data2:
        raw_file.write(''.join([str(cell) for cell in line]).replace("'b'", '').replace(r"\r\n", ','))
        raw_file.write('\r\n')

    raw_file.close()


"""
Connecting to imap.qiye.163.com
Logging in as mosoedu@chinahrt.com
Response code: OK
Server response: b'() "/" "INBOX"'
Server response: b'(\\Drafts) "/" "&g0l6P3ux-"'
Server response: b'(\\Sent) "/" "&XfJT0ZAB-"'
Server response: b'(\\Trash) "/" "&XfJSIJZk-"'
Server response: b'(\\Junk) "/" "&V4NXPpCuTvY-"'
Server response: b'() "/" "&dcVr0mWHTvZZOQ-"'
"""


