--file-trust-verifier--
Project Overview

This project implements a Python-based Command Line Interface (CLI) tool designed to ensure both the integrity and authenticity of files. The tool combines SHA-256 hashing and RSA digital signatures, allowing a sender to sign a set of files and a receiver to verify that the files have not been altered and indeed come from the sender.

The workflow is simple and effective:

Hash all files in a directory and store the hashes in a manifest (metadata.json).
Generate a RSA key pair (private and public keys).
Sign the manifest using the private key.
Verify the manifest and file integrity using the public key.

This system ensures tamper detection and non-repudiation, which are critical in secure file transfer and trusted environments.

1. Why Hashing Alone Isn’t Enough

SHA-256 is a cryptographic hash function that produces a unique 256-bit digest for any given file. Its main properties include:

Deterministic: The same file always produces the same hash.
Collision-resistant: Two different files are highly unlikely to produce the same hash.
Sensitive to changes: Any modification, even a single bit, results in a completely different hash.

While hashing ensures integrity, it cannot prove the origin of a file. An attacker could modify both a file and its hash, making it appear authentic.

Key point: Hashing alone does not prevent malicious tampering and cannot provide non-repudiation.

2. How Digital Signatures Enhance Security

Digital signatures address the limitations of hashing by introducing cryptographic identity verification:

The sender generates a private/public RSA key pair.
The SHA-256 hash of the manifest (metadata.json) is encrypted with the private key, producing a digital signature.
The receiver uses the sender’s public key to decrypt the signature and verify it against the manifest hash.

This mechanism ensures:

Integrity: Any change in the manifest or files invalidates the signature.
Authenticity: Only the owner of the private key could have created the signature.
Non-repudiation: The sender cannot deny having signed the files, preventing disputes.

By combining hashing and digital signatures, the tool provides a secure and lightweight method for verifying file authenticity.

3. Implementation Details

The CLI tool provides three main commands:

Setup: Generates RSA keys (private_key.pem and public_key.pem).
Sign: Scans a directory (test_folder), computes SHA-256 hashes for each file, creates a metadata.json manifest, and signs it using the private key.
Verify: Checks the manifest signature using the public key and compares each file’s current hash with the manifest to detect tampering.

Key Python libraries used:

hashlib – For SHA-256 hashing.
cryptography – For RSA key generation, signing, and verification.
os and json – For file management and manifest creation.

The tool prints clear messages to indicate:

Successful key generation, signing, and verification.
Missing files or unauthorized modifications.
Signature validity and overall integrity status.

4. Demonstration and Use Case

This tool is useful in situations where:

Sensitive files need to be shared over untrusted channels.
Data integrity is critical (e.g., legal documents, financial reports).
A simple, automated way to verify file authenticity is required.

Live demo workflow:

Signing a file set → signature created.
Modifying one file → verification fails with a warning.
The tool distinguishes between unaltered and tampered files, demonstrating reliability.
5. Conclusion

This project highlights the importance of combining hash functions and digital signatures to achieve both integrity and authenticity.

While SHA-256 alone ensures file integrity, RSA digital signatures guarantee the source of the data and prevent repudiation.

The Python CLI tool provides an easy-to-use, end-to-end solution for file verification, making it suitable for both educational purposes and practical use in secure file-sharing scenarios.

Demo Video

YouTube Link: [Insert Your Video Link Here]
