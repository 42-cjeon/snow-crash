password: 25749xKZ8L7DkSCwJkT9dyv6f

# 접근 방법

주어진 level09를 실행하면 인자로 들어온 문자열에 대해서 어떤 규칙을 적용하고 새로운 문자열로 변환하여 다시 출력해주는 것을 볼 수 있다.
이때 입력으로 000000000000000을 넣게 되었을 때 출력 문자열은 0123456789:;<=>인 것을 볼 수 있는데, 따라서 규칙은 각 문자의 인덱스에 해당하는 값만큼 더해주는 것이다.

따라서 그것을 복호화할 프로그램을 만들고, 주어진 token을 복호화 하면 된다

```bash
cat token | python2 -c "print(''.join(map(lambda x: chr(ord(x[1]) - x[0]), enumerate(open('/dev/stdin').read()[:-1]))))"
```