# IP ping

A [`ping(8)`](https://linux.die.net/man/8/ping) like tool using IP layer packets, currently only UDP is supported.

## UDP

Sends UDP packets to a running UDP echo server.

### Echo server

Echo server must be running on the machine we want to ping.

Using [`socat(1)`](https://linux.die.net/man/1/socat)

```sh
socat PIPE udp-recvfrom:5554,fork
```

Using [`nc(1)`](https://linux.die.net/man/1/nc)

```sh
nc -kule /bin/cat 5554
```

### Example usage

```sh
$ ipping udp 192.168.20.2 5554 -i 0.5 -s 8176 -c 4
PING 192.168.20.2:5554: 8176 data bytes
8192 bytes from 192.168.20.2:5554: time=7.476 ms
8192 bytes from 192.168.20.2:5554: time=7.687 ms
8192 bytes from 192.168.20.2:5554: time=13.941 ms
8192 bytes from 192.168.20.2:5554: time=8.448 ms

--- 192.168.20.2:5554 ping statistics ---
4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 7.476/9.388/13.941/3.064 ms
```
