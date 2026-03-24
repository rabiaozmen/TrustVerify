# 🛡️ TrustVerify

## 📖 Project Overview
This project implements a **Python-based Command Line Interface (CLI)** tool designed to ensure both the **integrity** and **authenticity** of files. The tool combines **SHA-256 hashing** and **RSA digital signatures**, allowing a sender to sign a set of files and a receiver to verify that the files have not been altered and indeed come from the sender.

### The Workflow:
1. **Hash** all files in a directory and store the hashes in a manifest (`metadata.json`).
2. **Generate** an RSA key pair (private and public keys).
3. **Sign** the manifest using the private key.
4. **Verify** the manifest and file integrity using the public key.

This system ensures **tamper detection** and **non-repudiation**, which are critical in secure file transfer and trusted environments.

---

## ❓ Why Hashing Alone Isn’t Enough
SHA-256 is a cryptographic hash function that produces a unique 256-bit digest for any given file. Its main properties include:
* **Deterministic:** The same file always produces the same hash.
* **Collision-resistant:** Two different files are highly unlikely to produce the same hash.
* **Sensitive to changes:** Any modification, even a single bit, results in a completely different hash.

> **Key point:** While hashing ensures integrity, it cannot prove the **origin** of a file. An attacker could modify both a file and its hash, making it appear authentic. Hashing alone does not prevent malicious tampering and cannot provide **non-repudiation**.

---

## 🔐 How Digital Signatures Enhance Security
Digital signatures address the limitations of hashing by introducing cryptographic identity verification:
1. The sender generates a **private/public RSA key pair**.
2. The SHA-256 hash of the manifest (`metadata.json`) is encrypted with the **private key**, producing a digital signature.
3. The receiver uses the sender’s **public key** to decrypt the signature and verify it against the manifest hash.

### This mechanism ensures:
* **Integrity:** Any change in the manifest or files invalidates the signature.
* **Authenticity:** Only the owner of the private key could have created the signature.
* **Non-repudiation:** The sender cannot deny having signed the files, preventing disputes.

---

## 🛠 Implementation Details
The CLI tool provides three main commands:

| Command | Description |
| :--- | :--- |
| **Setup** | Generates RSA keys (`private_key.pem` and `public_key.pem`). |
| **Sign** | Scans `test_folder`, computes SHA-256 hashes, creates `metadata.json`, and signs it. |
| **Verify** | Checks the signature and compares each file's current hash with the manifest. |

**Key Python libraries used:** `hashlib`, `cryptography`, `os`, and `json`.

---

## 🚀 Demonstration and Use Case
This tool is useful for sharing sensitive files over untrusted channels or where data integrity is critical (legal/financial docs).

### Live Demo Workflow:
* **Signing:** A signature is created for the file set.
* **Tampering:** Modifying even one file causes verification to fail with a warning.
* **Result:** The tool clearly distinguishes between unaltered and tampered files, demonstrating reliability.

---

## 🎓 Conclusion
This project highlights the importance of combining **hash functions** and **digital signatures** to achieve both integrity and authenticity. While SHA-256 alone ensures file integrity, RSA digital signatures guarantee the source of the data and prevent repudiation.
