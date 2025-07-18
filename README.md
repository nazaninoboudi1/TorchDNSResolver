# 🚀 TorchDNSResolver

**A Python script to resolve IP addresses to domain names from MikroTik Torch active connections.**

---

## 📝 Overview

**TorchDNSResolver** monitors real-time network traffic on a MikroTik router using the RouterOS API, extracts destination IP addresses from active firewall connections, and resolves them to domain names.  
It uses DNS reverse lookups first and falls back to WHOIS queries to provide organization information if DNS resolution fails.  

This tool helps network administrators and penetration testers gain better visibility into traffic flows by converting raw IPs into meaningful hostnames or organization names.

---

## ✨ Features

- ⚡ Real-time monitoring of MikroTik firewall connections  
- 🔍 Reverse DNS (PTR) lookup for IP-to-domain resolution  
- 🕵️ WHOIS lookup fallback to fetch organization names  
- 🧵 Multi-threaded for efficient and fast processing  
- 🗃️ Caching of resolved IPs to reduce redundant lookups  
- ⚙️ Configurable scan interval and connection parameters

---

## 📋 Requirements

- 🐍 Python 3.x  
- 🌐 MikroTik RouterOS with API enabled  
- 📦 Python package: `routeros-api`  
- 🛠️ WHOIS command-line tool installed on your OS  

---

## ⚙️ Installation

1. **Install Python 3** (if not already installed)  
2. **Install required Python package:**  
```bash
pip install routeros-api
```
---

## 🛠 MikroTik Router Setup
- Enable the API Service:
- Connect to your MikroTik router using Winbox or SSH.
- Navigate to IP > Services.
- Ensure the api service is enabled (default port 8728).
- Create a Read-Only User for API Access:
- Run this command in the MikroTik terminal:
/user add name=monitor group=read password=your_secure_password
- Replace monitor and your_secure_password with your preferred username and strong password.
- Using a read-only user improves security by limiting access.

---
## ⚙️ How It Works
- Connects to the MikroTik RouterOS API using provided credentials.
- Fetches active connections from /ip/firewall/connection.
- Extracts the destination IP address from each connection entry.
- Performs a DNS reverse lookup (PTR) on the IP.
- If DNS lookup fails, performs a WHOIS query to fetch organization details.
- Caches all resolved IPs for faster repeated lookups.
- Runs DNS/WHOIS lookups in multiple threads to improve speed.
- Displays IP-to-domain mappings in real-time on the console.

---
## 👤 Author

**Nazanin Oboudi**

