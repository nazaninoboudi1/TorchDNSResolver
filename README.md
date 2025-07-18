# TorchDNSResolver
A Python script to resolve IP addresses to domain names for MikroTik Torch monitoring


# MikroTik IP to Domain Resolver 🧠

This Python script resolves IP addresses captured by MikroTik's Torch tool into human-readable domain names.  
It helps network admins and penetration testers to monitor traffic more effectively by mapping raw IPs to hostnames.

## 🔧 Features
- Real-time IP to domain resolution
- Uses `socket.gethostbyaddr()` for reverse DNS lookup
- Simple and lightweight script

## 📦 Requirements
- Python 3.x
- MikroTik RouterOS access
- Torch output (via Winbox or SSH)

## 🚀 Usage
1. Export IPs from MikroTik Torch.
2. Run the script:
   ```bash
   python ip2domain.py
