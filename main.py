import hashlib
import json
import os
import sys
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# 1. FILE HASHING (SHA-256)
def generate_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

# 2. CREATE MANIFEST (LIST)
def create_manifest(directory_path):
    manifest = {}
    if not os.path.exists(directory_path):
        print(f"❌ Error: Directory {directory_path} not found!")
        return
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            manifest[filename] = generate_file_hash(file_path)
            
    with open("metadata.json", "w") as f:
        json.dump(manifest, f, indent=4)
    print(f"✅ Manifest created: metadata.json ({len(manifest)} files)")

# 3. GENERATE KEYS (RSA)
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    public_key = private_key.public_key()
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("🔑 Keys generated: private_key.pem and public_key.pem")

# 4. SIGN MANIFEST
def sign_manifest():
    if not os.path.exists("private_key.pem") or not os.path.exists("metadata.json"):
        print("❌ Error: Run setup and sign first!")
        return

    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    with open("metadata.json", "rb") as f:
        manifest_data = f.read()

    signature = private_key.sign(
        manifest_data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    with open("signature.sig", "wb") as f:
        f.write(signature)
    print("✍️ metadata.json signed (signature.sig).")

# 5. VERIFY TRUST (CRITICAL PART)
def verify_trust():
    try:
        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        with open("signature.sig", "rb") as f:
            signature = f.read()
        with open("metadata.json", "rb") as f:
            manifest_data = f.read()
    except FileNotFoundError:
        print("❌ Error: Required files (keys, signature or JSON) missing!")
        return

    # SIGNATURE VERIFICATION
    try:
        public_key.verify(
            signature, manifest_data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("✅ Signature Valid: Manifest truly comes from you.")
    except:
        print("❌ ERROR: Invalid signature! Seal has been broken.")
        return

    # FILE VERIFICATION
    with open("metadata.json", "r") as f:
        manifest = json.load(f)

    tampered = False
    for filename, old_hash in manifest.items():
        file_path = os.path.join("test_folder", filename)
        if not os.path.exists(file_path):
            print(f"❌ Error: {filename} file is missing!")
            tampered = True
            continue
        
        if generate_file_hash(file_path) != old_hash:
            print(f"⚠️ WARNING: {filename} HAS BEEN TAMPERED! (Data Tampering)")
            tampered = True

    if not tampered:
        print("🛡️ All files are safe, integrity preserved.")

# --- COMMAND LINE CONTROL ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python main.py [setup | sign | verify]")
    else:
        cmd = sys.argv[1].lower()
        if cmd == "setup": generate_keys()
        elif cmd == "sign":
            create_manifest("test_folder")
            sign_manifest()
        elif cmd == "verify": verify_trust()
        else: print("Unknown command!")