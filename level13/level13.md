> Password: g1qKMiRpXf53AWhDaU7FEkczr

# 접근 방법

홈 디렉토리의 `level13` 프로그램을 실행시켜보면

```bash
$ ./level13
UID 2013 started us but we we expect 4242
```

사용자의 `UID`가 `4242`가 아니여서 실행할 수 없다고 나온다.

gdb를 사용해서 `main` 함수의 어셈블리 코드르 확인하면
```
(gdb) disas main
Dump of assembler code for function main:
   0x0804858c <+0>:	push   ebp
   0x0804858d <+1>:	mov    ebp,esp
   0x0804858f <+3>:	and    esp,0xfffffff0
   0x08048592 <+6>:	sub    esp,0x10
   0x08048595 <+9>:	call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    eax,0x1092
   0x0804859f <+19>:	je     0x80485cb <main+63>
   0x080485a1 <+21>:	call   0x8048380 <getuid@plt>
   0x080485a6 <+26>:	mov    edx,0x80486c8
   0x080485ab <+31>:	mov    DWORD PTR [esp+0x8],0x1092
   0x080485b3 <+39>:	mov    DWORD PTR [esp+0x4],eax
   0x080485b7 <+43>:	mov    DWORD PTR [esp],edx
   0x080485ba <+46>:	call   0x8048360 <printf@plt>
   0x080485bf <+51>:	mov    DWORD PTR [esp],0x1
   0x080485c6 <+58>:	call   0x80483a0 <exit@plt>
   0x080485cb <+63>:	mov    DWORD PTR [esp],0x80486ef
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
   0x080485d7 <+75>:	mov    edx,0x8048709
   0x080485dc <+80>:	mov    DWORD PTR [esp+0x4],eax
   0x080485e0 <+84>:	mov    DWORD PTR [esp],edx
   0x080485e3 <+87>:	call   0x8048360 <printf@plt>
   0x080485e8 <+92>:	leave
   0x080485e9 <+93>:	ret
End of assembler dump.
```

매우 간단하게 `UID`가 `4242(0x1092)`와 일치하는지 확인한 후 `ft_des`라는 함수를 실행한 결과를 그대로 출력하는 코드인 것을 알 수 있다.

따라서 `UID`를 확인하는 부분만 우회하면 그대로 토큰이 출력될 것으로 예상된다.

`gdb`에서 `main`함수에 브레이크 포인트를 걸고, 실행한 후 현재 실행중인 라인을 가르키는 레지스터 `eip`를 `UID` 확인이 끝난 위치인 `0x080485cb`으로 변경하고 실행을 재개하면 토큰을 얻을 수 있다.

```
(gdb) b main
Breakpoint 1 at 0x804858f
(gdb) r
Starting program: /home/user/level13/level13

Breakpoint 1, 0x0804858f in main ()
=> 0x0804858f <main+3>:	83 e4 f0	and    esp,0xfffffff0
(gdb) set $eip = 0x080485cb
(gdb) c
Continuing.
your token is 2A31L79asukciNyi8uppkEuSx

Program received signal SIGSEGV, Segmentation fault.
0x0804b008 in ?? ()
=> 0x0804b008:	32 41 33	xor    al,BYTE PTR [ecx+0x33]
```