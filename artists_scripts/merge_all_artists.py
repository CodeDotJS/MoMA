import os
import json

def merge_json_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "artists.json")

    all_data = []
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
            all_data.extend(data)

    with open(output_file, 'w') as outfile:
        json.dump(all_data, outfile, indent=2)

    print(f"All JSON files merged and saved as artists.json in {output_folder}")

if __name__ == "__main__":
    input_folder = "../Files/Artists/ExtendedCollection"
    output_folder = "../"
    merge_json_files(input_folder, output_folder)
