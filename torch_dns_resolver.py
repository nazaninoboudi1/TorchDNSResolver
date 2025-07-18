#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Real-Time MikroTik Traffic IP Resolver
--------------------------------------
Monitors active MikroTik firewall connections and resolves destination IPs to domain names,
with a fallback to WHOIS-based organization information when reverse DNS is unavailable.

Author: YourName
GitHub: https://github.com/nazaninoboudi1/TorchDNSResolver
License: MIT
"""

import routeros_api
import socket
import time
import threading
import subprocess
import re
import argparse

# ================= Default Settings =================
DEFAULT_SCAN_INTERVAL = 5       # Time between scans in seconds
MAX_THREADS = 20                # Maximum concurrent threads
ip_seen = set()                 # Track IPs already processed to avoid duplicates
lock = threading.Lock()         # Thread lock for thread-safe counters
active_threads = 0              # Number of currently running threads
cache = {}                     # Cache for resolved IPs to avoid repeated lookups

# ================= IP Resolution Function =================
def resolve_ip(ip):
    """
    Resolves an IP address to a domain name using:
    1) PTR DNS reverse lookup
    2) WHOIS lookup for organization info if PTR fails
    Caches results to improve performance.
    """
    if ip in cache:
        return cache[ip]

    # Attempt reverse DNS (PTR) lookup
    try:
        domain = socket.gethostbyaddr(ip)[0]
        cache[ip] = domain
        return domain
    except socket.herror:
        pass

    # Fallback to WHOIS lookup for organization name
    try:
        whois_data = subprocess.check_output(
            ['whois', ip],
            timeout=5,
            stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='ignore')

        match = re.search(r'(?i)(OrgName|Org|netname|descr|owner):\s*(.+)', whois_data)
        if match:
            domain_guess = match.group(2).strip()
            cache[ip] = f"[WHOIS: {domain_guess}]"
            return cache[ip]
    except Exception:
        pass

    # If all fails, mark as not found
    cache[ip] = "❌ Not Found"
    return cache[ip]

# ================= IP Processing Thread =================
def process_ip(ip):
    """
    Thread target function to resolve an IP and print the result.
    Manages the active_threads count with thread safety.
    """
    global active_threads
    with lock:
        active_threads += 1
    try:
        domain = resolve_ip(ip)
        print(f"{ip:>15} ➜ {domain}")
    finally:
        with lock:
            active_threads -= 1

# ================= Main Monitoring Function =================
def start_monitoring(mt_ip, username, password, interval):
    """
    Connects to MikroTik RouterOS API and monitors active firewall connections.
    Resolves new destination IP addresses in real time using multi-threading.
    """
    global active_threads
    print(f"🔌 Connecting to MikroTik RouterOS at {mt_ip} ...")

    try:
        connection = routeros_api.RouterOsApiPool(
            mt_ip,
            username=username,
            password=password,
            plaintext_login=True
        )
        api = connection.get_api()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    conn_resource = api.get_resource('/ip/firewall/connection')
    print("🎯 Real-time traffic monitoring started (Ctrl+C to stop):\n")

    while True:
        try:
            connections = conn_resource.get()
            for conn in connections:
                dst_ip = conn.get('dst-address', '').split(':')[0]
                if dst_ip and dst_ip not in ip_seen:
                    ip_seen.add(dst_ip)

                    # Limit number of concurrent threads
                    while active_threads >= MAX_THREADS:
                        time.sleep(0.1)

                    threading.Thread(
                        target=process_ip,
                        args=(dst_ip,),
                        daemon=True
                    ).start()

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(interval)

# ================= Script Entry Point =================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time MikroTik traffic IP resolver with DNS/WHOIS fallback.")
    parser.add_argument("--ip", help="MikroTik Router IP address", default="192.168.88.1")
    parser.add_argument("--user", help="MikroTik username", default="monitor")
    parser.add_argument("--pass", help="MikroTik password", default="123456")
    parser.add_argument("--interval", help="Scan interval in seconds", type=int, default=DEFAULT_SCAN_INTERVAL)
    args = parser.parse_args()

    start_monitoring(args.ip, args.user, args.pass, args.interval)
