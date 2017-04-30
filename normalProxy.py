import sys
import socket
import threading


def serverLoop(local_host,local_port,remote_host,remote_port,receive_first):

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))
    except:
        print ('failed to listen')
        sys.exit(0)
    print ('listening...')

    server.listen(5)

    while True:
        client_socket,addr = server.accept()

        print ('connection from %s,%d' %(addr[0],addr[1]))

        # start thread to receive and send to remote host
        proxy_thread = threading.Thread(target=proxyHandler
                                        ,args=(client_socket,remote_host
                                               ,remote_port,receive_first))
        proxy_thread.start()


def proxyHandler(client_socket, remote_host, remote_port, receive_first):

    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buff = receiveFrom(remote_socket)
        hexdump(remote_buff)
        remote_buff = responseHandler(remote_buff)

        if len(remote_buff):
            print ('sending %d bytes to localhost' %len(remote_buff))
            client_socket.send(remote_buff)

    while True:
        local_buff = receiveFrom(client_socket)

        if len(local_buff):
            print ('received %d bytes from localhost' %len(local_buff))
            hexdump(local_buff)
            local_buff = requestHandler(local_buff)
            remote_socket.send(local_buff)
            print ('sending to remote server')

        remote_buff = receiveFrom(remote_socket)

        if len(remote_buff):
            print ('received %d bytes from remote server' %len(remote_buff))
            hexdump(remote_buff)
            remote_buff = responseHandler(remote_buff)
            client_socket.send(remote_buff)
            print ('sending to localhost')
        #commented for trying purposes
        #if not len(local_buff) or not len(remote_buff):
         #   client_socket.close()
          #  remote_socket.close()
           # print ('bye connection i will miss you')
            #break

#turn buffer to hex 'n text taken as it is
def hexdump(source,length=16):
    result = []
    digits = 4 if isinstance(source, unicode) else 2
    for i in xrange(0,len(source),length):
        s = source[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length * (digits + 1), hexa, text))
    print (b'\n'.join(result))

def receiveFrom(connection):
    buff = ''
    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buff += data
    except:
        pass
    return buff

def requestHandler(buffer):

    return buffer

def responseHandler(buffer):

    return buffer

def main():

    #we need 5 args to start checking them
    if len(sys.argv[1:]) != 5:
        print ("Usage: ./normalProxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    serverLoop(local_host,local_port,remote_host,remote_port,receive_first)
main()