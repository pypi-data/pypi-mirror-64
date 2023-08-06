# tcping

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
  --help                 Show this message and exit.
```

## Example

```shell
mtcping -i hosts.txt -p ports.txt -t 30
```

## Released

### v0.1.0

- First release.