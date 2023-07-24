import json

def extract_and_save_artists(json_file_path, txt_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    artists_set = set(artwork["Artist"] for artwork in data)

    with open(txt_file_path, 'w') as file:
        for artist in artists_set:
            file.write(artist + '\n')

def split_names_and_remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        artists = file.read().splitlines()

    split_artists = []
    for artist in artists:
        split_names = artist.split(', ')
        split_artists.extend(split_names)

    unique_artists = list(set(split_artists))

    unique_artists.sort()

    with open(file_path, 'w') as file:
        for artist in unique_artists:
            file.write(artist + '\n')

json_file_path = '../artworks.json'
txt_file_path = '../artists.txt'
extract_and_save_artists(json_file_path, txt_file_path)
split_names_and_remove_duplicates(txt_file_path)
