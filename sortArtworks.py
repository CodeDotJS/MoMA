import json

with open('artworks.json', 'r') as file:
    artworks_data = json.load(file)

for artwork in artworks_data:
    artwork['ObjectID'] = int(artwork['ObjectID'])

sorted_artworks_data = sorted(artworks_data, key=lambda x: x['ObjectID'])

with open('artworks.json', 'w') as file:
    json.dump(sorted_artworks_data, file, indent=4)

print("Artworks sorted by ObjectID and saved to artworks.json")
