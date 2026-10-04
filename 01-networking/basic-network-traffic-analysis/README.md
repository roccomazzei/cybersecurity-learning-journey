# Lab 01 — Basic Network Traffic Analysis

**Path:** TryHackMe Cyber Security 101  
**Section:** Networking  
**Environment:** Kali Linux virtual machine  
**Tools:** tcpdump, Wireshark, dig, curl, iproute2

## Objective

The goal of this lab was to reinforce the networking concepts covered in Cyber Security 101 by generating a small amount of controlled traffic, capturing it, and inspecting the packets.

The activity focused on:

- identifying the active interface, local IP address, and default gateway
- observing ICMP Echo Request / Echo Reply traffic
- examining DNS queries and responses
- comparing HTTP and HTTPS connections
- identifying TCP source and destination ports
- recognizing the TCP three-way handshake

## Lab Environment

The Kali Linux VM was connected through the `eth0` interface.

- **Local IPv4 address:** `10.211.55.5/24`
- **Default gateway / DNS resolver:** `10.211.55.1`
- **Local network:** `10.211.55.0/24`

> The addresses shown here belong to an isolated virtualized lab network.

### Network configuration



## Traffic Generation

Traffic was generated intentionally using standard networking tools.

### DNS lookup

A DNS query was generated with:

```bash
dig example.com
```

The resolver used by the VM was `10.211.55.1`. The query returned IPv4 addresses for `example.com`.


### HTTP and HTTPS

HTTP and HTTPS requests were generated with:

```bash
curl -I http://example.com
curl -I https://example.com
```

The HTTP request used TCP port 80, while the HTTPS request used TCP port 443.


## Packet Analysis

The traffic was captured with `tcpdump` and analyzed in Wireshark.

The packet capture itself is **not published** in this repository. The write-up records only the relevant observations from the controlled lab traffic.

### ICMP

Using the Wireshark display filter:

```text
icmp
```

I identified ICMP Echo Requests sent from the Kali VM to the default gateway and the corresponding Echo Replies.

This reinforced the request/reply behavior used by `ping` and showed that ICMP works directly over IP rather than using TCP or UDP ports.


### DNS

Using the filter:

```text
dns
```

I identified DNS queries from the Kali VM to the resolver on port 53 and the corresponding responses.

The packet details show the client using an ephemeral source port and destination port `53`.


### TCP Three-Way Handshake

For the HTTP connection, the capture clearly showed the TCP connection establishment sequence:

1. **SYN** — the client requests a new connection.
2. **SYN, ACK** — the server acknowledges the request.
3. **ACK** — the client acknowledges the server response.

In the captured HTTP connection, the Kali VM used ephemeral source port `59864` and connected to destination port `80`.

The HTTPS connection used the same TCP handshake concept before TLS communication began on destination port `443`.


## Key Takeaways

This lab connected several networking concepts into one practical workflow:

- the default gateway provides the route outside the local subnet
- ICMP can be used to test basic IP reachability
- DNS translates names into IP addresses and normally uses destination port 53
- clients typically use temporary high-numbered source ports when connecting to services
- HTTP and HTTPS use TCP but differ at the application/security layer
- TCP establishes a reliable connection using the SYN → SYN/ACK → ACK handshake
- Wireshark display filters make it easier to isolate specific protocols from a larger capture

## SOC / Defensive Security Relevance

Packet analysis is useful in defensive security because an analyst may need to determine:

- which host initiated a connection
- which service and destination port were contacted
- whether name resolution occurred before a connection
- whether a TCP connection was successfully established
- whether unexpected ICMP, DNS, or web traffic is present

This lab provides a basic foundation for later traffic-analysis and SOC investigations.

## Ethics and Scope

All traffic in this exercise was generated from my own Kali Linux lab environment using normal network requests. No unauthorized scanning or testing was performed.
