import ipaddress
import subprocess
import sys
import argparse
import time

parser = argparse.ArgumentParser(
    description="Check if an IP address is reachable")

parser.add_argument("-i", "--ip", help="IP address to check", required=True)
args = parser.parse_args()

cidr = args.ip


def pinger(ip):
    start_time = time.time()

    process = subprocess.run(["ping", "-c", "1", "-W", "0.1", ip], stdout=subprocess.DEVNULL)

    end_time = time.time()
    
    elapsed = end_time - start_time
    
    if process.returncode == 0:
        return ("UP", elapsed)
    elif process.returncode == 1:
        return ("DOWN", elapsed)
    else:
        return ("ERROR", None)

try:
    network = ipaddress.ip_network(cidr, strict=False)
except:
    print("Bad CIDR")
    sys.exit(1)

up = 0
down = 0
errors = 0
hosts = 0

for host in network.hosts():
    hosts += 1
    host = str(host)
    status, elapsed = pinger(host)

    if status == "UP":
        up += 1
        print(f"{host:15} - UP    ({elapsed}ms)")
    elif status == "DOWN":
        down += 1
        print(f"{host:15} - DOWN  ({elapsed}ms)")
    else:
        errors += 1
        print(f"{host:15} - ERROR (Connection timeout)")

print("\nScan complete.")
print(f"Found {up} active hosts, {down} down, and {errors} error")
print(f"Total scanned: {hosts} addresses.")

