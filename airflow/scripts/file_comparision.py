import hashlib
import os

def calculate_file_hash(file_path):
    #calculates the MD5 hash of the file contents.
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read();
        hasher.update(buf)
    return hasher.hexdigest()

def has_file_changed(file_path, hash_storage_path):
    # checking if the file has changed by comparing the hashses.
    current_hash = calculate_file_hash(file_path)
    
    if os.path.exists(hash_storage_path):
        with open(hash_storage_path, 'r') as f:
            saved_hash = f.read().strip()
    else:
        saved_hash = None

    if current_hash != saved_hash:
        with open(hash_storage_path, 'w') as f:
            f.write(current_hash)
        return True
    return False

file_path = "/opt/airflow/Scrapped_data/data.txt"
hash_storage_path = "/opt/airflow/Scrapped_data/last_file_hash.txt"
if has_file_changed(file_path, hash_storage_path):
    print("changed")
else:
    print("not changed")






