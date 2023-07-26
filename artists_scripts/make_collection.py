import os
import json

def merge_json_files(folder_path, output_file):
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

    combined_data = []

    for file in json_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            combined_data.extend(data)

    with open(output_file, 'w') as output_json_file:
        json.dump(combined_data, output_json_file, indent=4)

folder_path = '../Files/Artists/Collection'
output_file = '../artists.json'
merge_json_files(folder_path, output_file)
