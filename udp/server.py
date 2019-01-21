from socket import *

host = 'localhost'
port = 777
addr = (host,port)

  # socket_family: AF_INET or AF_UNIX
  # socket_type: SOCK_STREAM(TCP) or SOCK_DGRAM(UDP)
udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)

while True:
    question = input('Do you want to quit? y\\n: ')
    if question == 'y': break
    
    print('wait data...')
    
    conn, addr = udp_socket.recvfrom(1024)
    print('client addr: ', addr)
    udp_socket.sendto(b'message received by the server', addr)
    
udp_socket.close()
print('socket close')