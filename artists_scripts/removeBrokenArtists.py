import json

def remove_objects_with_null_data(input_file, output_file, broken_file):
    with open(input_file, 'r') as input_json_file:
        data = json.load(input_json_file)

    valid_objects = []
    broken_objects = []

    for obj in data:
        if obj['bio'] is None or obj['details'] is None:
            broken_objects.append(obj)
        else:
            valid_objects.append(obj)

    with open(output_file, 'w') as output_json_file:
        json.dump(valid_objects, output_json_file, indent=4)

    with open(broken_file, 'w') as broken_json_file:
        json.dump(broken_objects, broken_json_file, indent=4)

input_file = '../artists.json'
output_file = 'artists.json'
broken_file = 'brokenArtists.json'
remove_objects_with_null_data(input_file, output_file, broken_file)
