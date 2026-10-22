<p align="center">
  <img src="assets/cybersecurity-journey-banner.svg" alt="Cybersecurity Learning Journey banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cyber%20Security%20101-Final%20block-22c55e?style=for-the-badge" alt="Cyber Security 101 final block">
  <img src="https://img.shields.io/badge/Current-OWASP%20Top%2010-f59e0b?style=for-the-badge" alt="Current focus OWASP Top 10">
  <img src="https://img.shields.io/badge/Next-SOC%20Level%201-0ea5e9?style=for-the-badge" alt="Next SOC Level 1">
</p>

# Cybersecurity Learning Journey

Hands-on cybersecurity portfolio focused on **TryHackMe**, selected practical labs, and the skills I am building toward an entry-level **SOC Analyst** role.

> [!NOTE]
> This repository is intentionally **not** a collection of copied walkthroughs. I document selected exercises that demonstrate practical skills, troubleshooting, security analysis, and investigation.

## 🎯 Current Focus

**TryHackMe — Cyber Security 101**

All main sections are completed through defensive-security tooling. The remaining block is **OWASP Top 10**.

After Cyber Security 101, the next major path will be **TryHackMe SOC Level 1**, where selected investigations will be promoted to portfolio labs.

## 🧭 Learning Map

| Area | Status | Main skills / tools | Portfolio work |
|---|:---:|---|---|
| 🖥️ [Foundations](00-foundations/) | ✅ | Linux, Windows, AD, CMD, PowerShell | Fundamentals |
| 🌐 [Networking](01-networking/) | ✅ | TCP/IP, DNS, Nmap, Wireshark, tcpdump | [Lab 01](01-networking/basic-network-traffic-analysis/) |
| 🔐 [Cryptography](02-cryptography/) | ✅ | Hashing, Hashcat, John, OpenSSL, AES, RSA | [Lab 02](02-cryptography/cryptography-and-password-security/) |
| 💥 [Exploitation](03-exploitation/) | ✅ | Metasploit, payloads, sessions, Meterpreter | Selected practice |
| 🌍 [Web Security](04-web-security/) | ✅ | HTTP, SQL, Burp Suite | Lab 03 planned |
| 🛠️ [Offensive Tooling](05-offensive-security-tooling/) | ✅ | Hydra, Gobuster, shells, SQLMap | Lab 03 planned |
| 🛡️ [Defensive Security](06-defensive-security/) | ✅ | SOC, logs, IR, forensics | Foundations |
| 📡 [Security Solutions](07-security-solutions/) | ✅ | SIEM, firewall, IDS/IPS, vuln scanning | Foundations |
| 🔬 [Defensive Tooling](08-defensive-security-tooling/) | ✅ | CyberChef, CAPA, REMnux, FlareVM | Foundations |
| ⚠️ [OWASP Top 10](09-owasp-top-10/) | 🟡 | Web application risks | Current focus |
| 🔵 [SOC Level 1](10-soc-level-1/) | ⏭️ | Triage, SIEM, endpoint/network monitoring | Next path |

## 🧪 Portfolio Labs

### 01 · Basic Network Traffic Analysis
Packet and protocol analysis with **Wireshark** and **tcpdump**, covering ICMP, DNS, HTTP/HTTPS, TCP handshakes, addressing, routing, and neighbour discovery.

➡️ **[Open Lab 01](01-networking/basic-network-traffic-analysis/)**

### 02 · Cryptography and Password Security
Hands-on work with **SHA-256**, **Hashcat**, salted password hashes, **AES**, **RSA**, and digital signatures.

➡️ **[Open Lab 02](02-cryptography/cryptography-and-password-security/)**

### 03 · Web Application Security Assessment
Planned portfolio assessment combining **Burp Suite**, web fundamentals, offensive tooling, and **OWASP** concepts in an authorized lab environment.

> [!IMPORTANT]
> A full lab is created only when the exercise adds clear portfolio value. The goal is quality over quantity.

## 🧰 Toolset

**Systems**  
`Linux` · `Windows` · `Active Directory` · `PowerShell`

**Network & Traffic**  
`Nmap` · `Wireshark` · `tcpdump`

**Offensive Security**  
`Burp Suite` · `Metasploit` · `Gobuster` · `Hydra` · `SQLMap`

**Cryptography & Password Security**  
`OpenSSL` · `Hashcat` · `John the Ripper`

**Defensive Analysis**  
`SIEM concepts` · `IDS/IPS` · `CyberChef` · `CAPA` · `REMnux` · `FlareVM`

## 🛣️ Direction

```text
Cyber Security 101
        ↓
Web Application Security Assessment
        ↓
SOC Level 1
        ↓
Selected SOC Investigation Labs
        ↓
SOC Analyst / Incident Response
```

Detailed system-administration work is kept in my separate **IT Systems Administration Labs** repository to avoid duplication.
