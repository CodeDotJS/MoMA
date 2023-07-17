import json

with open("artworks.json", "r") as f:
    json_data = json.load(f)

keys = {}

for item in json_data:
    other_keys = list(json_data[0].keys())
    for key in other_keys:
        if key in item:
            keys[key] = keys.get(key, 0) + 1

for key, count in keys.items():
    print(f"Total '{key}' objects: {count}")
