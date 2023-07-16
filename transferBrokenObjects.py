import json
import re

with open('artworks.json', 'r') as file:
    data = json.load(file)

# excluding 'State/variant'
non_word_pattern = re.compile(r'(?<!State/)^\W|(?<=State/)^\W')

# Store the flawed objects
broken_objects = []
objects_to_remove = []

for index, obj in enumerate(data):
    details = obj.get('Details', {})
    has_flaw = any(non_word_pattern.search(key) for key in details)
    if has_flaw:
        broken_objects.append(obj)
        objects_to_remove.append(index)

# Save the broken objects to "brokendata.json" file
with open('PagesBroken/brokendata.json', 'w') as output_file:
    json.dump(broken_objects, output_file, indent=2)

# Remove the identified objects from the data
for index in reversed(objects_to_remove):
    data.pop(index)

# Save the modified data back to "artworks.json" file
with open('artworks.json', 'w') as output_file:
    json.dump(data, output_file, indent=2)
