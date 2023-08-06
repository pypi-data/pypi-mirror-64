# echo-server

Network service that send messages back to client. Used in network testing.

## Install

```shell
pip install echo-server
```

### Installed Commands

- echo-server

### Usage

```shell
[root@test ~]# echo-server --help
Usage: echo-server [OPTIONS] [PORT]...

  Start echo server on given ports. Press CTRL+C to stop. The default
  listenning port is 3682. You can listen on many ports at the same time.

  Example:

  echo-server 8001 8002 8003

Options:
  --help  Show this message and exit.
```


## Releases

### v0.1.1 2020/03/27

- Fix port str typed problem.

### v0.1.0 2020/03/27

- First release