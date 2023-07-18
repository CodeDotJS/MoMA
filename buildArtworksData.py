import json
import glob
import os
import shutil

directories = ["Files/ExtendedCollection/", "Files/PagesFixed/"]

combined_data = []

for directory in directories:
    json_files = glob.glob(os.path.join(directory, "extended_*_MoMA.json"))

    for file in json_files:
        if directory == "Files/PagesFixed/":
            if not os.path.exists(directories[0]):
                os.makedirs(directories[0])
            shutil.move(file, os.path.join(directories[0], os.path.basename(file)))

json_files = glob.glob(os.path.join(directories[0], "extended_*_MoMA.json"))
for file in json_files:
    with open(file, "r") as f:
        json_data = json.load(f)
        combined_data.extend(json_data)

other_directory_files = glob.glob(os.path.join(directories[1], "*.json"))
for file in other_directory_files:
    os.remove(file)

script_directory = os.getcwd()
output_file = os.path.join(script_directory, "artworks.json")
with open(output_file, "w") as f:
    json.dump(combined_data, f, indent=4)

print("Files combined and artworks.json saved successfully.")
