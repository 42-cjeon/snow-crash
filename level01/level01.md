> Password: x24ti5gi3x0ol2eh4esiuxias

# 접근 방법

`level00`을 해결하는 과정에서 `/etc/passwd` 파일을 확인했는데
`flag01` 계정의 비밀번호가 노출되어 있는 것을 확인함.

비밀번호는 `42hDRfypTqqnw`였고 해시된 상태였음.

`/etc/pam.d/passwd`를 확인하여 `unix crypt`이 기본 해시 알고리즘이라는 것을 알아냈고, 그 중에서도 맨 앞 두글자 `42`를 `salt`로 사용하는 `des`기반의 해시 알고리즘인 것도 확인함.

이후 `john the ripper`프로그램을 이용한 무차별 대입을 통해서 flag가 `abcdefg`인 것을 확인함.
