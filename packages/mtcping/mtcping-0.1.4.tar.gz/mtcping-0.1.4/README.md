# mtcping

Do tcping on many targets.

## Install

```shell
pip install mtcping
```

## Installed Command Utils

- mtcping


## Usage

```shell
[root@testsvr tmp]# mtcping --help
Usage: mtcping [OPTIONS] [PORT]...

Options:
  -t, --timeout INTEGER
  -i, --hosts-file TEXT  [required]
  -p, --ports-file TEXT
  -r, --retry INTEGER
  --help                 Show this message and exit.
```

## Example

```shell
C:\Code\mtcping>mtcping -i hosts.txt -p ports.txt
www.google.com   80    is closed
www.google.com   443   is closed
www.baidu.com    443   is open
www.qq.com       80    is open
www.qq.com       443   is open
www.baidu.com    80    is open

C:\Code\mtcping>type hosts.txt
www.baidu.com
www.qq.com
www.google.com

C:\Code\mtcping>type ports.txt
80
443

C:\Code\mtcping>mtcping -i hosts.txt 80 443
www.google.com   80    is closed
www.google.com   443   is closed
www.baidu.com    80    is open
www.baidu.com    443   is open
www.qq.com       443   is open
www.qq.com       80    is open

```

- We can load ports list from a file or form command arguments.
- We can load hosts list from a file or read from stdin.
  - Use "-" or "stdin" to read from sys.stdin. For example: `mtcping -i stdin 80`.

## Released

### v0.1.4 2020/04/01

- Add retry option.

### v0.1.3 2020/04/01

- Fix document.

### v0.1.2 2020/04/01

- Fix requirements.txt, remove all version.

### v0.1.1 2020/04/01

- Fix requirements.txt, use click<7.0 instead of click~=6.7, so that it can work for python2.6.

### v0.1.0 2020/04/01

- First release.