#!/usr/bin/env python3
"""
crypto_toolkit.py
------------------
Small security toolkit for ETTCS801 - Cryptography & Network Security.

Features:
  1. Encrypt a file (AES via Fernet - authenticated symmetric encryption)
  2. Decrypt a file and verify contents match the original
  3. Compute a SHA-256 hash and detect later tampering
  4. Handle missing files / invalid input gracefully (no crashes)

IMPORTANT: Never commit the generated key file (secret.key) to GitHub.
Add it to .gitignore. Use only sample/dummy student data, never real
records.

Usage:
    python crypto_toolkit.py genkey
    python crypto_toolkit.py encrypt <input_file> <output_file>
    python crypto_toolkit.py decrypt <input_file> <output_file>
    python crypto_toolkit.py hash <file>
    python crypto_toolkit.py verify <file> <saved_hash_file>
"""

import sys
import os
import hashlib
import argparse

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    print("Missing dependency. Install it with: pip install cryptography")
    sys.exit(1)

KEY_FILE = "secret.key"


def generate_key():
    """Generate and save a new encryption key (kept OUTSIDE the repo)."""
    key = Fernet.generate_key()
    try:
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print(f"[OK] Key generated and saved to {KEY_FILE}")
        print("    Remember: add this file to .gitignore, never push it.")
    except OSError as e:
        print(f"[ERROR] Could not write key file: {e}")
        sys.exit(1)


def load_key():
    if not os.path.exists(KEY_FILE):
        print(f"[ERROR] Key file '{KEY_FILE}' not found. Run 'genkey' first.")
        sys.exit(1)
    try:
        with open(KEY_FILE, "rb") as f:
            return f.read()
    except OSError as e:
        print(f"[ERROR] Could not read key file: {e}")
        sys.exit(1)


def encrypt_file(input_path, output_path):
    if not os.path.isfile(input_path):
        print(f"[ERROR] Input file '{input_path}' does not exist.")
        sys.exit(1)

    key = load_key()
    fernet = Fernet(key)

    try:
        with open(input_path, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"[ERROR] Could not read '{input_path}': {e}")
        sys.exit(1)

    encrypted = fernet.encrypt(data)

    try:
        with open(output_path, "wb") as f:
            f.write(encrypted)
    except OSError as e:
        print(f"[ERROR] Could not write '{output_path}': {e}")
        sys.exit(1)

    print(f"[OK] Encrypted '{input_path}' -> '{output_path}'")


def decrypt_file(input_path, output_path):
    if not os.path.isfile(input_path):
        print(f"[ERROR] Input file '{input_path}' does not exist.")
        sys.exit(1)

    key = load_key()
    fernet = Fernet(key)

    try:
        with open(input_path, "rb") as f:
            token = f.read()
    except OSError as e:
        print(f"[ERROR] Could not read '{input_path}': {e}")
        sys.exit(1)

    try:
        decrypted = fernet.decrypt(token)
    except InvalidToken:
        print("[ERROR] Decryption failed: invalid key or corrupted/tampered file.")
        sys.exit(1)

    try:
        with open(output_path, "wb") as f:
            f.write(decrypted)
    except OSError as e:
        print(f"[ERROR] Could not write '{output_path}': {e}")
        sys.exit(1)

    print(f"[OK] Decrypted '{input_path}' -> '{output_path}'")


def compute_hash(file_path):
    if not os.path.isfile(file_path):
        print(f"[ERROR] File '{file_path}' does not exist.")
        sys.exit(1)

    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
    except OSError as e:
        print(f"[ERROR] Could not read '{file_path}': {e}")
        sys.exit(1)

    digest = sha256.hexdigest()
    hash_file = file_path + ".sha256"
    with open(hash_file, "w") as f:
        f.write(digest)

    print(f"[OK] SHA-256 of '{file_path}':")
    print(f"     {digest}")
    print(f"[OK] Saved to '{hash_file}'")
    return digest


def verify_hash(file_path, saved_hash_file):
    if not os.path.isfile(file_path):
        print(f"[ERROR] File '{file_path}' does not exist.")
        sys.exit(1)
    if not os.path.isfile(saved_hash_file):
        print(f"[ERROR] Saved hash file '{saved_hash_file}' does not exist.")
        sys.exit(1)

    with open(saved_hash_file, "r") as f:
        original_hash = f.read().strip()

    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    current_hash = sha256.hexdigest()

    if current_hash == original_hash:
        print("[OK] Integrity check PASSED - file has not been modified.")
        return True
    else:
        print("[ALERT] Integrity check FAILED - file has been modified!")
        print(f"    Expected: {original_hash}")
        print(f"    Got:      {current_hash}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Encryption & integrity toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("genkey", help="Generate a new encryption key")

    p_enc = sub.add_parser("encrypt", help="Encrypt a file")
    p_enc.add_argument("input_file")
    p_enc.add_argument("output_file")

    p_dec = sub.add_parser("decrypt", help="Decrypt a file")
    p_dec.add_argument("input_file")
    p_dec.add_argument("output_file")

    p_hash = sub.add_parser("hash", help="Compute SHA-256 hash of a file")
    p_hash.add_argument("file")

    p_verify = sub.add_parser("verify", help="Verify a file against a saved hash")
    p_verify.add_argument("file")
    p_verify.add_argument("saved_hash_file")

    args = parser.parse_args()

    if args.command == "genkey":
        generate_key()
    elif args.command == "encrypt":
        encrypt_file(args.input_file, args.output_file)
    elif args.command == "decrypt":
        decrypt_file(args.input_file, args.output_file)
    elif args.command == "hash":
        compute_hash(args.file)
    elif args.command == "verify":
        verify_hash(args.file, args.saved_hash_file)


if __name__ == "__main__":
    main()
