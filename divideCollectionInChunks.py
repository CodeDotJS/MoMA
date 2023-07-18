import os
import json

input_file = "Files/data/collection.json"
save_in = "Files/Collection_Pages"

with open(input_file, "r") as file:
    data = json.load(file)

if not os.path.exists(save_in):
    os.makedirs(save_in)

for key, value in data.items():
    filename = f"{save_in}/{key}_MoMA.json"
    with open(filename, "w") as file:
        json.dump(value, file, indent=4)
