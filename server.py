import socket
import sys
from thread import *


def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return "".join(enc)


def decode(key, enc):
    dec = []
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    # Sending message to connected client
    key = '123'
    #conn.send(encode(key,'Welcome to the server. Type something and hit enter\n'))  # send only takes string
    conn.send('Welcome to the server. Type something and hit enter\n')
    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        data = conn.recv(1024)
        #data = decode(key,data)
        reply = 'OK...' + data
        if not data:
            break

        #conn.sendall(encode(key,reply))
        conn.sendall(reply)

    # came otut of loop
    conn.close()

def main():

    if len(sys.argv[1:]) != 2:
        print ("Usage: ./server.py [HOST] [PORT]")
        sys.exit(0)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

# Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

# Start listening on socket
    s.listen(10)
    print 'Socket now listening'

# now keep talking with the client
    while 1:
    # wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread, (conn,))

main()
