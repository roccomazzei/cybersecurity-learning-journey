# File Integrity and Hashing Lab

## Overview

This laboratory demonstrates how SHA-256 hashes can be used to verify file integrity and detect unauthorized modifications.

A file was created, hashed, modified, and checked against its original checksum. The laboratory shows that even a small change to a file produces a completely different cryptographic hash.

## Objectives

* Calculate SHA-256 hashes on macOS
* Establish a trusted baseline for a file
* Verify file integrity automatically
* Detect an unauthorized file modification
* Restore a file and confirm its integrity
* Understand the avalanche effect of cryptographic hash functions

## Laboratory Environment

* Operating system: macOS
* Shell: Zsh
* Hashing utility: `shasum`
* Algorithm: SHA-256
* Version control: Git and GitHub

> All commands in this laboratory were executed from the root directory of the `cybersecurity-learning-journey` repository.

## Project Structure

```text
file-integrity-and-hashing/
├── README.md
├── hashes/
│   ├── modified-sha256.txt
│   ├── original-sha256.txt
│   └── tampered-sha256.txt
├── samples/
│   ├── modified.txt
│   └── original.txt
└── screenshots/
```

## Procedure

### 1. Create the original file

```bash
printf "This is the original file.\n" > samples/original.txt
```

### 2. Calculate the original SHA-256 hash

```bash
shasum -a 256 samples/original.txt
```

Original SHA-256:

```text
56d9fc4585da4f39bbc5c8ec953fb7962188fa5ed70b2dd5a19dc82df997ba5e
```

### 3. Create a modified version

```bash
printf "This is the modified file.\n" > samples/modified.txt
```

Modified SHA-256:

```text
a26d3ba465dfa3dd11b163ac317b6abe91fcc429cb72242ca4099bf9cfdb0f63
```

The hashes are completely different even though the files differ by only one word. This demonstrates the avalanche effect.

### 4. Verify the original file

```bash
shasum -a 256 -c hashes/original-sha256.txt
```

Expected result:

```text
samples/original.txt: OK
```

### 5. Simulate an unauthorized modification

```bash
printf "Unauthorized change.\n" >> samples/original.txt
```

The integrity check then returned:

```text
samples/original.txt: FAILED
shasum: WARNING: 1 computed checksum did NOT match
```

### 6. Restore and verify the file

The original content was restored:

```bash
printf "This is the original file.\n" > samples/original.txt
```

The integrity verification returned:

```text
samples/original.txt: OK
```

## Results

The laboratory successfully demonstrated that:

* a SHA-256 hash represents the exact contents of a file;
* changing the file changes its hash;
* the original checksum can be used as a trusted baseline;
* an integrity check can detect that a modification occurred;
* an integrity check does not explain what was changed or who changed it.

## Security Relevance

File integrity monitoring can help detect:

* unauthorized changes to configuration files;
* modification of system binaries;
* website defacement;
* malware altering legitimate files;
* corruption during storage or transmission;
* unexpected changes to sensitive documents.

A hash alone does not prove that a file is trustworthy. The reference hash must come from a trusted and protected source.

## Security+ Concepts

This laboratory relates to the following concepts:

* data integrity;
* hashing;
* cryptographic algorithms;
* file integrity monitoring;
* security baselines;
* change detection;
* incident detection.

## Key Takeaways

* Hashing is not encryption.
* SHA-256 produces a fixed-length digest.
* Hashes are highly sensitive to input changes.
* Identical files produce identical hashes.
* Different hashes prove that file contents differ.
* Hash verification depends on the trustworthiness of the baseline.

## Ethical Statement

All activities in this laboratory were performed on locally created files in a personal and authorized environment.

