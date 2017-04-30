import socket
import sys

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


def main():
    if len(sys.argv[1:]) != 2:
        print ("Usage: ./client.py [HOST] [PORT]")
        sys.exit(0)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.connect(server_address)


    while True:
        key='123'
        # Receiving from client
        data = sock.recv(4096)
        #data = decode(key, data)
        print data
        reply = raw_input("Please enter something: ")
        #sock.sendall(encode(key, reply))
        sock.sendall(reply)
main()