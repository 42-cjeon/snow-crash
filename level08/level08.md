> Password: fiumuikeil55xe9cu4dood66h

# 접근 방법

```bash
$ ls -l
total 16
-rwsr-s---+ 1 flag08 level08 8617 Mar  5  2016 level08
-rw-------  1 flag08 flag08    26 Mar  5  2016 token
```

홈 디렉토리를 확인했을 때, `level08` 바이너리와 `token`텍스트 파일이 있는 것을 볼 수 있고, `token`에 대한 권한이 제한적이라는 점, `level08`에 `set GID/UID`가 설정되어있다는 점을 통해 시작지점을 `level08`으로 잡음.

`objdump`를 통해 본 `main`함수의 어셈블리가 매우 복잡해 보이지만, 대부분 시스템 콜 실패 시의 처리와, 인자 개수 확인 등 예외 처리에 치중되어 있고 핵심 부분은 프로그램의 첫 번째 인자와 문자열 `"token"`을 `strstr`을 통해서 비교하여, 같을 경우 프로그램 실행을 거부하는 부분임.

```asm
 80485ba:	e8 41 fe ff ff       	call   8048400 <strstr@plt>
 80485bf:	85 c0                	test   %eax,%eax
 80485c1:	74 26                	je     80485e9 <main+0x95>
```

따라서 인자로 직접 들어가는 이름은 `token`이 아니지만 실제로는 `~/token`파일을 가르키는 심볼릭 링크를 생성하여 `strstr`을 우회할 수 있음.

```bash
$ ln -s ~/token /tmp/level08
$ ~/level08 /tmp/level08
```