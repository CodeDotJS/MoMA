import os
import json
import shutil

folder_path = "ExtendedCollection/"
broken_folder_path = "PagesBroken/"

if not os.path.exists(broken_folder_path):
    os.makedirs(broken_folder_path)

json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]

for json_file in json_files:
    file_path = os.path.join(folder_path, json_file)

    with open(file_path, "r") as file:
        json_data = json.load(file)

    if isinstance(json_data, list):
        for index, obj in enumerate(json_data):
            if "Details" not in obj:
                print(f"{json_file}: Object at index {index} does not contain 'Details'")
                shutil.move(file_path, os.path.join(broken_folder_path, json_file))
                break
    elif "Details" not in json_data:
        print(f"{json_file}: Object does not contain 'Details'")
        shutil.move(file_path, os.path.join(broken_folder_path, json_file))
