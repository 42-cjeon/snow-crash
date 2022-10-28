> Password: level00

# 접근 방법

- 환경 변수 확인
- bash 설정 파일 확인
- 쉘 히스토리
- `/etc/passwd`에 노출된 비밀번호
- `flag00` 유저가 소유한 모든 파일 검색

이때 마지막 방법에서

`/usr/sbin/john`이라는 수상한 파일을 찾게 되었고 `sbin`에 있음에도
실행 권한이 없고 단순 읽기 권한만이 있는것이 수상해서 `cat`으로 읽어보니

`cdiiddwpgswtgt`이라는 문자열이 나왔고, 이 문자열을 카이사르 암호 (키: 15)로 복호화하여 `nottoohardhere`이라는 암호를 획득함.

```bash
find / -not -path "./proc/*" -a -not -path "./rofs/*" -a -user flag00 2> /dev/null | xargs cat | tr '[p-za-o]' '[a-z]'
```
