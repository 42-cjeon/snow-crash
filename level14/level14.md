> Password: 2A31L79asukciNyi8uppkEuSx

# 접근 방법

아무런 힌트가 없어서 지금까지 플래그를 얻기 위해 사용했던 `getflag`실행 파일을 직접 공격해보자. 일단 `objdump`을 이용해서 어셈블리를 확인하면 상당히 긴 코드가 나온다. 또한 `gdb`나 `strace`등의 동적 디버그 도구를 통해서 실행했을 경우 `You should not reverse this`라는 출력이 나오는 것을 볼 수 있다.

`main`함수의 앞부분은 동적 디버깅을 막기 위한 부분과 `dynamic library injection`을 막기 위해 있는 부분으로 이루어져 있다.

그 부분을 넘어가면 `getuid`를 호출하여 프로그램을 실행한 유저를 알아내고, 각각 `UID`에 따라 분기를 하는 부분이 있다.

```asm
8048afd:	e8 ae f9 ff ff       	call   80484b0 <getuid@plt>
8048b02:	89 44 24 18          	mov    %eax,0x18(%esp)
8048b06:	8b 44 24 18          	mov    0x18(%esp),%eax
8048b0a:	3d be 0b 00 00       	cmp    $0xbbe,%eax
8048b0f:	0f 84 b6 01 00 00    	je     8048ccb <main+0x385>
8048b15:	3d be 0b 00 00       	cmp    $0xbbe,%eax
8048b1a:	77 4c                	ja     8048b68 <main+0x222>
8048b1c:	3d ba 0b 00 00       	cmp    $0xbba,%eax
8048b21:	0f 84 14 01 00 00    	je     8048c3b <main+0x2f5>
8048b27:	3d ba 0b 00 00       	cmp    $0xbba,%eax
8048b2c:	77 1f                	ja     8048b4d <main+0x207>
8048b2e:	3d b8 0b 00 00       	cmp    $0xbb8,%eax
8048b33:	0f 84 ba 00 00 00    	je     8048bf3 <main+0x2ad>
8048b39:	3d b8 0b 00 00       	cmp    $0xbb8,%eax
8048b3e:	0f 87 d3 00 00 00    	ja     8048c17 <main+0x2d1>
8048b44:	85 c0                	test   %eax,%eax
8048b46:	74 7e                	je     8048bc6 <main+0x280>
8048b48:	e9 b9 02 00 00       	jmp    8048e06 <main+0x4c0>
8048b4d:	3d bc 0b 00 00       	cmp    $0xbbc,%eax
8048b52:	0f 84 2b 01 00 00    	je     8048c83 <main+0x33d>
8048b58:	3d bc 0b 00 00       	cmp    $0xbbc,%eax
8048b5d:	0f 87 44 01 00 00    	ja     8048ca7 <main+0x361>
8048b63:	e9 f7 00 00 00       	jmp    8048c5f <main+0x319>
8048b68:	3d c2 0b 00 00       	cmp    $0xbc2,%eax
8048b6d:	0f 84 e8 01 00 00    	je     8048d5b <main+0x415>
8048b73:	3d c2 0b 00 00       	cmp    $0xbc2,%eax
8048b78:	77 1b                	ja     8048b95 <main+0x24f>
8048b7a:	3d c0 0b 00 00       	cmp    $0xbc0,%eax
8048b7f:	0f 84 8e 01 00 00    	je     8048d13 <main+0x3cd>
8048b85:	3d c0 0b 00 00       	cmp    $0xbc0,%eax
8048b8a:	0f 87 a7 01 00 00    	ja     8048d37 <main+0x3f1>
8048b90:	e9 5a 01 00 00       	jmp    8048cef <main+0x3a9>
8048b95:	3d c4 0b 00 00       	cmp    $0xbc4,%eax
8048b9a:	0f 84 03 02 00 00    	je     8048da3 <main+0x45d>
8048ba0:	3d c4 0b 00 00       	cmp    $0xbc4,%eax
8048ba5:	0f 82 d4 01 00 00    	jb     8048d7f <main+0x439>
8048bab:	3d c5 0b 00 00       	cmp    $0xbc5,%eax
8048bb0:	0f 84 0e 02 00 00    	je     8048dc4 <main+0x47e>
8048bb6:	3d c6 0b 00 00       	cmp    $0xbc6,%eax
8048bbb:	0f 84 24 02 00 00    	je     8048de5 <main+0x49f>
8048bc1:	e9 40 02 00 00       	jmp    8048e06 <main+0x4c0>
```

따라서 `flag14`의 `UID`에 해당하는 `3014(0xbc6)`와 `eax`를 비교하는 부분을 찾으면
```
8048bb6:	3d c6 0b 00 00       	cmp    $0xbc6,%eax
8048bbb:	0f 84 24 02 00 00    	je     8048de5 <main+0x49f>
```

`0x8048de5`위치로 점프한다는 것을 알 수 있고,

```
8048de5:	a1 60 b0 04 08       	mov    0x804b060,%eax
8048dea:	89 c3                	mov    %eax,%ebx
8048dec:	c7 04 24 20 92 04 08 	movl   $0x8049220,(%esp)
8048df3:	e8 0c f8 ff ff       	call   8048604 <ft_des>
8048df8:	89 5c 24 04          	mov    %ebx,0x4(%esp)
8048dfc:	89 04 24             	mov    %eax,(%esp)
8048dff:	e8 2c f7 ff ff       	call   8048530 <fputs@plt>
```

그곳에서는 `ft_des`를 호출한 결과를 `fputs`으로 출력하는 것을 알 수 있는데 `token`을 출력하는 부분일 가능성이 높아 보인다.

따라서 gdb를 이용해서 같은 인자로 `ft_des`를 호출하고, 결과를 확인해보면 `token`을 얻을 수 있다.

```bash
(gdb) b main
Breakpoint 1 at 0x804894a
(gdb) r
Starting program: /bin/getflag

Breakpoint 1, 0x0804894a in main ()
(gdb) print (const char *)ft_des(0x8049220)
$1 = 0x804c008 "7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ"
```

---
## Alternative Method
---
`getflag` 바이너리를 직접 역공학으로 분석하는 대신, flag14의 권한으로 속이는 방법을 시도해볼 수 있다.


1. 먼저, `scp`를 사용해 `/bin/getflag` 바이너리를 snow-crash 밖으로 가지고 온다.
    ```
    scp -P 4242 level00@192.168.56.3:/bin/getflag .
    ```

2. snow-crash에서, `/etc/passwd` 파일을 참조해서, `flag14`가 몇 번의 gid 및 uid를 사용하고 있는 지 확인한다.
    ```bash
    $ cat /etc/passwd
    root:x:0:0:root:/root:/bin/bash
    [...]
    level14:x:2014:2014::/home/user/level14:/bin/bash
    [...]
    flag14:x:3014:3014::/home/flag/flag14:/bin/bash
    ```
    여기에서, `flag14`는 `3014`의 gid 및 uid를 가지는 것을 확인할 수 있다.

3. root 권한을 가진 x86(i386) 환경을 준비한다. `scp`로 가지고 온 `getflag` 바이너리를 전달하는 것도 잊으면 안된다. (여기서는 `Docker`에서 `i386/ubuntu` 이미지 사용.)
    ```
    $ docker run -it -v /Users/smun/sc/getflag:/getflag i386/ubuntu
    WARNING: The requested image's platform (linux/386) does not match the detected host platform (linux/amd64) and no specific platform was requested
    root@ef34540df8e8:/#
    ```

4. gid 3014를 가지는 그룹, uid 3014를 가지는 그룹을 생성한다.
    ```
    # addgroup --gid 3014 flag14
    Adding group `flag14' (GID 3014) ...
    Done.
    # adduser --gid 3014 --uid 3014 flag14
    Adding user `flag14' ...
    Adding new user `flag14' (3014) with group `flag14' ...
    [...]
    ```

5. 생성된 `flag14` 계정 및 그룹의 ID를 확인해본다.
    ```
    # id -u flag14
    3014
    # id -g flag14
    3014
    ```

6. 생성된 `flag14` 계정으로 로그인 후, `getflag` 바이너리를 실행한다.
    ```
    # su flag14
    $ ./getflag
    Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
    $
    ```

7. snow-crash에서 해당 token을 사용하여 `flag14`에 로그인해본다.
    ```
    level14@SnowCrash:~$ su flag14
    Password:
    Congratulation. Type getflag to get the key and send it to me the owner of this livecd :)
    flag14@SnowCrash:~$
    ```
