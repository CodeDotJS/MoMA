import os
import json

with open("collection.json", "r") as file:
    data = json.load(file)

if not os.path.exists("separateCollection"):
    os.makedirs("separateCollection")

for key, value in data.items():
    filename = f"Collection_Pages/{key}_MoMA.json"
    with open(filename, "w") as file:
        json.dump(value, file, indent=4)
