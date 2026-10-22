<p align="right"><a href="README.md">🇬🇧 English</a> · <strong>🇮🇹 Italiano</strong></p>

# Lab 02 — Cryptography and Password Security

## Obiettivo

Questo lab consolida i concetti pratici della sezione **Cyber Security 101 — Cryptography** di TryHackMe. Gli esercizi sono stati svolti in un ambiente Kali Linux controllato e riguardano hashing, sicurezza delle password, cifratura simmetrica, cifratura asimmetrica e firme digitali.

## Ambiente

- Kali Linux virtual machine
- OpenSSL 3.0.3
- Hashcat 6.2.5
- John the Ripper 1.9.0-jumbo
- RockYou wordlist
- Parallels Desktop

## Parte 1 — Hashing e integrità

Un file di testo è stato sottoposto a SHA-256, poi modificato e nuovamente hashato.

I due digest risultano completamente diversi, mostrando l'avalanche effect e l'utilità degli hash crittografici per verificare l'integrità di un file.

Evidenze:

- [SHA-256 originale](evidence/original-sha256.txt)
- [SHA-256 modificato](evidence/modified-sha256.txt)
- [Screenshot](screenshots/02-sha256-integrity.jpg)

## Parte 2 — Password hashing e dictionary attack

Una password di test volutamente debole è stata usata per creare un hash SHA-256 raw. Hashcat mode `1400` con la wordlist RockYou ha recuperato correttamente la password.

Un secondo test ha utilizzato un hash Unix `sha512crypt` con salt. Anche Hashcat mode `1800` ha recuperato la password volutamente debole.

Questo dimostra perché gli hash general-purpose veloci non dovrebbero essere usati direttamente per conservare password e perché salt e schemi specifici per password sono importanti.

Evidenze:

- [Hash SHA-256 raw](evidence/raw-sha256.txt)
- [Hash sha512crypt](evidence/sha512crypt.txt)
- [Screenshot cracking SHA-256](screenshots/03-raw-sha256-crack.jpg)
- [Screenshot hash con salt](screenshots/04-salted-hash.jpg)

## Parte 3 — Cifratura simmetrica

Un messaggio plaintext è stato cifrato con **AES-256-CBC** tramite OpenSSL e PBKDF2, quindi decifrato con la stessa password.

Il confronto tra file originale e decifrato ha confermato il ripristino esatto del plaintext.

Evidenza:

- [Screenshot AES](screenshots/05-aes-encryption.jpg)

## Parte 4 — Crittografia RSA

È stata generata una coppia di chiavi RSA disposable da 2048 bit.

La chiave pubblica è stata usata per cifrare un breve messaggio con padding OAEP e la chiave privata per decifrarlo. Un confronto byte-for-byte ha confermato la corrispondenza con il messaggio originale.

La chiave privata **non è inclusa nella repository**.

Evidenza:

- [Screenshot RSA](screenshots/06-rsa-encrypt-decrypt.jpg)

## Parte 5 — Firme digitali

La chiave privata RSA è stata utilizzata per firmare un messaggio con SHA-256. La verifica con la chiave pubblica ha restituito `Verified OK`.

Una copia del messaggio è stata poi modificata e la verifica è fallita, dimostrando che una firma digitale può rilevare alterazioni e fornire integrità e autenticità.

Evidenza:

- [Screenshot verifica firma](screenshots/07-signature-verification.jpg)

## Verifica degli strumenti

- [Screenshot strumenti](screenshots/01-tools.jpg)

## Concetti chiave

- l'hashing fornisce controllo di integrità e non è cifratura reversibile
- una piccola modifica dell'input produce un digest crittografico molto diverso
- password deboli possono essere recuperate rapidamente se presenti in wordlist comuni
- i salt riducono l'efficacia degli attacchi precomputati e impediscono che password uguali producano automaticamente hash memorizzati uguali
- la cifratura simmetrica usa lo stesso segreto per cifrare e decifrare
- la crittografia asimmetrica separa operazioni con chiave pubblica e privata
- le firme digitali rilevano modifiche e forniscono autenticità senza nascondere il contenuto

## Sicurezza ed etica

Tutti gli hash, le chiavi e i file usati sono stati generati appositamente per l'apprendimento in un ambiente controllato. Non sono state usate credenziali reali o sistemi di terze parti.

La chiave privata RSA disposable e la password temporanea di cifratura non vengono pubblicate.
