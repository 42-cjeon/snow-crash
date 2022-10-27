from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_TCP, TCP_NODELAY, 0)
s.bind(("0.0.0.0", 6969))
s.listen(1)

input("PRESS ANY KEY TO CONTINUE")
print('a')

conn, _ = s.accept()
recv_data = conn.recv(1024)
print(recv_data)

conn, _ = s.accept()
recv_data = conn.recv(1024)
print(recv_data)

s.close()
