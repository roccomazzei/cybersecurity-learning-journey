# Lab 02 — Cryptography and Password Security

## Objective

This lab consolidates the practical concepts covered in the TryHackMe **Cyber Security 101 — Cryptography** section. The exercises were performed in a controlled Kali Linux environment and focus on hashing, password security, symmetric encryption, asymmetric encryption, and digital signatures.

## Environment

- Kali Linux virtual machine
- OpenSSL 3.0.3
- Hashcat 6.2.5
- John the Ripper 1.9.0-jumbo
- RockYou wordlist
- Parallels Desktop

## Part 1 — Hashing and Integrity

A text file was hashed with SHA-256, then modified and hashed again.

The two digests were completely different, demonstrating the avalanche effect and showing how cryptographic hashes can be used to verify file integrity.

Evidence:

- [Original SHA-256](evidence/original-sha256.txt)
- [Modified SHA-256](evidence/modified-sha256.txt)
- [Screenshot](screenshots/02-sha256-integrity.jpg)

## Part 2 — Password Hashing and Dictionary Attacks

A deliberately weak test password was used to create a raw SHA-256 hash. Hashcat mode `1400` and the RockYou wordlist recovered the password successfully.

A second test used a salted Unix `sha512crypt` hash. Hashcat mode `1800` also recovered the deliberately weak password.

This demonstrates why fast general-purpose hashes should not be used directly for password storage and why salts and password-specific hashing schemes matter.

Evidence:

- [Raw SHA-256 test hash](evidence/raw-sha256.txt)
- [sha512crypt test hash](evidence/sha512crypt.txt)
- [Raw SHA-256 cracking screenshot](screenshots/03-raw-sha256-crack.jpg)
- [Salted hash cracking screenshot](screenshots/04-salted-hash.jpg)

## Part 3 — Symmetric Encryption

A plaintext message was encrypted with **AES-256-CBC** using OpenSSL and PBKDF2, then decrypted with the same password.

The original and decrypted files were compared successfully, confirming that the decryption restored the original plaintext.

Evidence:

- [AES encryption/decryption screenshot](screenshots/05-aes-encryption.jpg)

## Part 4 — RSA Public-Key Cryptography

A disposable 2048-bit RSA key pair was generated for the lab.

The public key was used to encrypt a short message with OAEP padding, and the private key was used to decrypt it. A byte-for-byte comparison confirmed that the decrypted message matched the original.

The private key is intentionally **not included in this repository**.

Evidence:

- [RSA encryption/decryption screenshot](screenshots/06-rsa-encrypt-decrypt.jpg)

## Part 5 — Digital Signatures

The RSA private key was used to sign a message with SHA-256. Verification with the public key returned `Verified OK`.

A copy of the message was then modified. Verification failed, demonstrating that a digital signature can detect tampering and provide integrity and authenticity.

Evidence:

- [Signature verification screenshot](screenshots/07-signature-verification.jpg)

## Tools Verification

The lab environment and tool versions are documented here:

- [Tools screenshot](screenshots/01-tools.jpg)

## Key Takeaways

- Hashing provides integrity checking and is not reversible encryption.
- A small input change produces a substantially different cryptographic digest.
- Weak passwords can be recovered quickly when they appear in common wordlists.
- Salts make precomputed password-hash attacks less useful and prevent equal passwords from automatically producing equal stored hashes.
- Symmetric encryption uses the same secret for encryption and decryption.
- Asymmetric cryptography separates public and private key operations.
- Digital signatures detect modification and provide authenticity without hiding the message contents.

## Security and Ethics

All password hashes, keys, and files used in this lab were generated specifically for learning in a controlled environment. No real credentials or third-party systems were used.

The disposable RSA private key and temporary encryption password are not published.
