import socket
import threading
import queue
import sys
import random
import os


# Client Code
def ReceiveData(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass


def RunClient(serverIP):
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000, 10000)
    print('Client IP->' + str(host) + ' Port->' + str(port))
    server = (str(serverIP), 12345)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    name = input('SERVER: Please write your name here: ')
    if name == '':
        name = 'Guest' + str(random.randint(1000, 9999))
        print('SERVER: Your name is:' + name)
    else:
        print('SERVER: Hi ' + name + "! Please start chatting now. To quit, type in {quit}")
    s.sendto(name.encode('utf-8'), server)

    welcome = 'SERVER: '+name + ' has entered the chat!'
    s.sendto(welcome.encode('utf-8'), server)
    threading.Thread(target=ReceiveData, args=(s,)).start()
    while True:
        data = input()
        if data == '{quit}':
            goodbye = "SERVER: "+name + " has left the chat."
            s.sendto(goodbye.encode('utf-8'), server)
            print("Goodbye!")
            break
        elif data == '':
            continue
        if data != '{quit}':
            data = '[' + name + ']' + '->' + data
            s.sendto(data.encode('utf-8'), server)
    # s.sendto(data.encode('utf-8'), server)
    s.close()
    os._exit(1)


# Client Code Ends Here


# Server Code
def RecvData(sock, recvPackets):
    while True:
        data, addr = sock.recvfrom(1024)
        recvPackets.put((data, addr))


def RunServer():
    host = socket.gethostbyname(socket.gethostname())
    port = 12345
    print('Server hosting on IP-> ' + str(host))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    clients = set()
    recvPackets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=RecvData, args=(s, recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data, addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            if data.endswith('{quit}'):
                clients.remove(addr)
                continue
            print(str(addr) + data)
            for c in clients:
                if c != addr:
                    s.sendto(data.encode('utf-8'), c)
    s.close()


# Server Code Ends Here

if __name__ == '__main__':
    if len(sys.argv) == 1:
        RunServer()
    elif len(sys.argv) == 2:
        RunClient(sys.argv[1])
    else:
        print('Run Server:-> python Chat.py')
        print('Run Client:-> python Chat.py <ServerIP>')
