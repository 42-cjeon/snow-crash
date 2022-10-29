도커 빌드
```bash
docker build -t snow_crash .
```

필요한 파일 복사

level01
> Password: x24ti5gi3x0ol2eh4esiuxias
```bash
scp -P 4242 level01@[host]:/etc/passwd ./passwd
```

level02
> Password: f2av5il02puano7naaf6adaaf
```bash
scp -P 4242 level02@[host]:~/level02.pcap ./level02.pcap
```

도커 실행
```bash
docker run -it --rm -v$(pwd):/shared snow_crash
```

level01
```bash
john /shared/passwd
john /shared/passwd --show

```

level02
```bash
tshark -r "level02.pcap" -z follow,tcp,hex,0
```