# TorchDNSResolver
A Python script to resolve IP addresses to domain names for MikroTik Torch monitoring

# MikroTik IP to Domain Resolver 🧠

This Python script resolves IP addresses captured by MikroTik's Torch tool into human-readable domain names.  
It helps network admins and penetration testers to monitor traffic more effectively by mapping raw IPs to hostnames.

## 🔧 Features
- Real-time IP to domain resolution  
- Uses `socket.gethostbyaddr()` for reverse DNS lookup  
- Fallback to WHOIS lookup when DNS fails  
- Multi-threaded for better performance  
- Caches resolved IPs to avoid redundant lookups  
- Lightweight and easy to configure  

## 📦 Requirements
- Python 3.x  
- MikroTik RouterOS with API enabled  
- `routeros-api` Python package (`pip install routeros-api`)  
- `whois` CLI tool installed on your system  

## ⚙️ MikroTik Router Setup

### 1. Enable API Service
Make sure the API service is enabled on your MikroTik router:  
- Open Winbox or SSH to your router  
- Go to **IP > Services**  
- Verify **API** is enabled and running on port `8728`

### 2. Create a Read-Only API User
For security, create a dedicated user with read-only access:  
```shell
/user add name=monitor group=read password=your_secure_password
