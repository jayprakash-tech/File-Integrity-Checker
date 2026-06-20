import hashlib
import json
import os

BASELINE_FILE = "baseline_hashes.json"
TARGET_FILE = "sample_file.txt"

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def create_baseline(file_path):
    file_hash = calculate_sha256(file_path)
    baseline_data = {file_path: file_hash}

    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(baseline_data, f, indent=4)

    print("=" * 60)
    print("FILE INTEGRITY CHECKER")
    print("=" * 60)
    print(f"Baseline created for: {file_path}")
    print(f"SHA-256: {file_hash}")
    print(f"Baseline saved to: {BASELINE_FILE}")
    print("=" * 60)

def check_integrity(file_path):
    if not os.path.exists(BASELINE_FILE):
        print("Baseline file not found. Create baseline first.")
        return

    with open(BASELINE_FILE, "r", encoding="utf-8") as f:
        baseline_data = json.load(f)

    if file_path not in baseline_data:
        print("No stored baseline hash for this file.")
        return

    stored_hash = baseline_data[file_path]
    current_hash = calculate_sha256(file_path)

    print("=" * 60)
    print("FILE INTEGRITY CHECKER")
    print("=" * 60)
    print(f"Target file: {file_path}")
    print(f"Stored SHA-256 : {stored_hash}")
    print(f"Current SHA-256: {current_hash}")
    print("-" * 60)

    if stored_hash == current_hash:
        print("Status: File integrity verified. No changes detected.")
    else:
        print("Status: WARNING - File has been modified!")

    print("=" * 60)

def main():
    print("Choose an option:")
    print("1. Create baseline hash")
    print("2. Check file integrity")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        create_baseline(TARGET_FILE)
    elif choice == "2":
        check_integrity(TARGET_FILE)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
