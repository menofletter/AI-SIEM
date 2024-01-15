import psutil

for interface, addrs in psutil.net_if_addrs().items():
    print(f"Interface: {interface}")
    for addr in addrs:
        print(f"  Address: {addr.address}")