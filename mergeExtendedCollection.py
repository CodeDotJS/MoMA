import json
import glob
import os

combined_data = []

directory = "ExtendedCollection"
json_files = glob.glob(os.path.join(directory, "extended_*_MoMA.json"))

for file in json_files:
    with open(file, "r") as f:
        json_data = json.load(f)
        combined_data.extend(json_data)

script_directory = os.path.dirname(os.path.abspath(__file__))

output_file = os.path.join(script_directory, "artworks.json")
with open(output_file, "w") as f:
    json.dump(combined_data, f, indent=4)

print("JSON files combined successfully.")
