import socket
import select
import errno
import sys
import os

from GetData import *
from entropy import *
from FileManager import getMessage

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = "POMPOS"

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)


# Wait for user to input a message
message = getMessage()

# If message is not empty - send it
if message:
    print("You have sent a message based on data.txt to the receiver: ")
    print(message)
    print()
    print('STATISTICS:')
    print('-----------------------------')
    print('Message.txt:')
    fileSize = os.path.getsize('Message.txt')
    print('● File Size:', fileSize, " bytes")
    source = str(fileSize)
    (l,h) = hist(source);
    print('● Entropy:', entropy(h, l))
    print('-----------------------------')

    file = 'EncodedMessage.txt'
    f = open(file, 'r+')
    f.truncate(0)
    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)

    try:
        # Receive our "header" containing username length, it's size is defined and constant
        username_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(username_header):
            print('Connection closed by the server')
            sys.exit()

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

    while (os.stat('EncodedMessage.txt').st_size == 0):
        if (os.stat('EncodedMessage.txt').st_size != 0):
            print('-----------------------------')
            print('EncodedMessage.txt:')
            fileSize = os.path.getsize('EncodedMessage.txt')
            print('● File Size:', fileSize, " bytes")
            source = str(fileSize)
            (l,h) = hist(source);
            print('● Entropy:', entropy(h, l))
            print('-----------------------------')
            break