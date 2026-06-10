import hashlib
import json
import os

HASH_FILE = "hashes.json"

def calculate_hash(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

def scan_directory(directory):
    hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root,file)

            try:
                hashes[path] = calculate_hash(path)
            except Exception as e:
                print(f"Error reading {path}: {e}")

    return hashes

directory = input("Enter folder path: ")

current_hashes = scan_directory(directory)

if not os.path.exists(HASH_FILE):
    with open(HASH_FILE, "w") as f:
        json.dump(current_hashes, f, indent=4)

    print("Baseline created.")
else:
    with open(HASH_FILE, "r") as f:
        saved_hashes = json.load(f)

    for file_path, current_hash in current_hashes.items():

        if file_path not in saved_hashes:
            print(f"[NEW FILE] {file_path}")

        elif saved_hashes[file_path] != current_hash:
            print(f"[MODIFIED] {file_path}")

    for file_path in saved_hashes:
        if file_path not in current_hashes:
            print(f"[DELETED] {file_path}")