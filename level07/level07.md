> Password: wiok45aaoguiboiki2tuin6ub

# 접근 방법

홈 디렉토리의 level07을 gdb로 확인해 보니

```c
const char *s = getenv("LOGNAME");
asprintf(buf, "/env/echo %s");
system(buf);
```

같은 흐름이다.

따라서 환경 변수 LOGNAME를 `&& getflag`으로 바꿔주면 해결할 수 있다.
