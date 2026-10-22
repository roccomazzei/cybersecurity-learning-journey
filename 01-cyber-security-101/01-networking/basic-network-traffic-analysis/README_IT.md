<p align="right"><a href="README.md">🇬🇧 English</a> · <strong>🇮🇹 Italiano</strong></p>

# Lab 01 — Basic Network Traffic Analysis

**Percorso:** TryHackMe Cyber Security 101  
**Sezione:** Networking  
**Ambiente:** macchina virtuale Kali Linux  
**Strumenti:** tcpdump, Wireshark, dig, curl, iproute2

## Obiettivo

L'obiettivo del lab è consolidare i concetti di networking affrontati in Cyber Security 101 generando una piccola quantità di traffico controllato, catturandolo e analizzando i pacchetti.

L'attività si concentra su:

- identificazione dell'interfaccia attiva, dell'indirizzo IP locale e del default gateway
- osservazione del traffico ICMP Echo Request / Echo Reply
- analisi di query e risposte DNS
- confronto tra connessioni HTTP e HTTPS
- identificazione delle porte TCP sorgente e destinazione
- riconoscimento del TCP three-way handshake

## Ambiente di laboratorio

La VM Kali Linux era connessa tramite l'interfaccia `eth0`.

- **Indirizzo IPv4 locale:** `10.211.55.5/24`
- **Default gateway / resolver DNS:** `10.211.55.1`
- **Rete locale:** `10.211.55.0/24`

> Gli indirizzi mostrati appartengono a una rete virtualizzata e isolata di laboratorio.

## Generazione del traffico

Il traffico è stato generato intenzionalmente con normali strumenti di rete.

### Query DNS

```bash
dig example.com
```

Il resolver utilizzato dalla VM era `10.211.55.1`. La query ha restituito indirizzi IPv4 per `example.com`.

### HTTP e HTTPS

```bash
curl -I http://example.com
curl -I https://example.com
```

La richiesta HTTP utilizza TCP/80, mentre HTTPS utilizza TCP/443.

## Analisi dei pacchetti

Il traffico è stato catturato con `tcpdump` e analizzato in Wireshark.

Il file PCAP **non viene pubblicato** nella repository. Il write-up riporta solo le osservazioni rilevanti del traffico controllato.

### ICMP

Filtro Wireshark:

```text
icmp
```

Sono stati identificati ICMP Echo Request inviati dalla VM Kali al default gateway e i corrispondenti Echo Reply.

Questo mostra il comportamento request/reply usato da `ping` e conferma che ICMP opera direttamente su IP senza porte TCP o UDP.

### DNS

Filtro:

```text
dns
```

Sono state identificate query DNS dalla VM Kali verso il resolver sulla porta 53 e le relative risposte.

Il client utilizza una porta sorgente effimera e la porta destinazione `53`.

### TCP Three-Way Handshake

Per la connessione HTTP, la cattura mostra chiaramente:

1. **SYN** — il client richiede una nuova connessione.
2. **SYN, ACK** — il server conferma la richiesta.
3. **ACK** — il client conferma la risposta del server.

Nella connessione HTTP catturata, la VM Kali usava la porta sorgente effimera `59864` verso la porta destinazione `80`.

La connessione HTTPS usa lo stesso meccanismo TCP prima dell'avvio della comunicazione TLS sulla porta `443`.

## Concetti chiave

- il default gateway fornisce il percorso verso reti esterne alla subnet locale
- ICMP può essere usato per verificare la raggiungibilità IP
- DNS traduce i nomi in indirizzi IP e normalmente usa la porta destinazione 53
- i client usano tipicamente porte sorgente temporanee ad alto numero
- HTTP e HTTPS usano TCP ma differiscono a livello applicativo e di sicurezza
- TCP stabilisce una connessione affidabile tramite SYN → SYN/ACK → ACK
- i display filter di Wireshark permettono di isolare protocolli specifici

## Rilevanza SOC / Defensive Security

L'analisi dei pacchetti aiuta un analyst a determinare:

- quale host ha iniziato una connessione
- quale servizio e porta sono stati contattati
- se è avvenuta una risoluzione DNS prima della connessione
- se una connessione TCP è stata stabilita correttamente
- se è presente traffico ICMP, DNS o web inatteso

Questo lab crea una base utile per future investigation di traffic analysis e SOC.

## Etica e scope

Tutto il traffico è stato generato nel mio ambiente Kali Linux con normali richieste di rete. Non è stata eseguita alcuna scansione o attività non autorizzata.
