import click
import time
import socket
import os
from io import open
import threading

print_lock = threading.Lock()

def do_ping(host, port, timeout=5, retry=1):
    message = ""
    for i in range(0, retry):
        try:
            sock = socket.create_connection((host, port), timeout=timeout)
            sock.close()
            message = "{0:16s} {1:<5d} is open".format(host, port)
            break
        except socket.timeout:
            message = "{0:16s} {1:<5d} timeout".format(host, port)
            time.sleep(1)
        except:
            message = "{0:16s} {1:<5d} is closed".format(host, port)
            time.sleep(1)
    with print_lock:
        print(message)

@click.command(name="mtcping")
@click.option("-t", "--timeout", type=int, default=5)
@click.option("-i", "--hosts-file", required=True)
@click.option("-p", "--ports-file", required=False)
@click.option("-r", "--retry", type=int, default=1)
@click.argument("port", nargs=-1, type=int, required=False)
def do_mtcping(hosts_file, ports_file, port, timeout, retry):
    if hosts_file.lower() in ["-", "stdin"]:
        ips = [x.strip() for x in os.sys.stdin.readlines() if x.strip()]
    else:
        with open(hosts_file, "r", encoding="utf-8") as fobj:
            ips = [x.strip() for x in fobj.readlines() if x.strip()]
    
    ports = port or []
    if ports_file:
        with open(ports_file, "r", encoding="utf-8") as fobj:
            ports += [int(x.strip()) for x in fobj.readlines() if x.strip()]

    nothing = False
    if not ips:
        print("No hosts to ping.")
        nothing = True
    if not ports:
        print("No ports to ping.")
        nothing = True
    if nothing:
        os.sys.exit(1)

    for ip in ips:
        for port in ports:
            t = threading.Thread(target=do_ping, args=(ip, port, timeout, retry))
            t.start()

if __name__ == "__main__":
    do_mtcping()
