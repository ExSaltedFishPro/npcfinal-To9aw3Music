import os
import uuid
import random

target = uuid.uuid4().hex
for _ in range(8):
    target += random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
os.system(f"mkdir -p /root/.{target}")
os.system(f"touch /root/.{target}/flag")

try:
    with open(f"/root/.{target}/flag", "w") as f:
        f.write(os.environ.pop("FLAG", "flag{test_flag}"))
except:
    pass
with open("/readFlag.c", "r") as f:
    code = f.read()
with open("/readFlag.c", "w") as f:
    code = code.replace("REPLACE", target)
    f.write(code)