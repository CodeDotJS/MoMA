import json
import os

file_names = ["artworks.json", "artists.json"]

def count_keys(json_data):
    keys = {}
    for item in json_data:
        for key in item:
            keys[key] = keys.get(key, 0) + 1
    return keys

for file_name in file_names:
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            json_data = json.load(f)
            keys_count = count_keys(json_data)
            print(f"File: {file_name}")
            for key, count in keys_count.items():
                print(f"Total '{key}' objects: {count}")
            print("\n")
    else:
        print(f"File '{file_name}' not found.")
