from socket import *
from time import sleep

def accept_and_print(sock):
  conn, _ = sock.accept()
  recv_data = conn.recv(1024)
  print(recv_data.decode('ascii'))

with socket(AF_INET, SOCK_STREAM) as sock:
  sock.bind(("0.0.0.0", 6969))
  sock.listen(1)

  while True:
    sleep(1)
    accept_and_print(sock)