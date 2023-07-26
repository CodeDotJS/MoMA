# Building Dataset

*Run the scripts in the given order.*

### Artworks Dataset

- __`artwork_collection.py`__ - It extracts artwork data from multiple pages of the Museum of Modern Art's collection The extracted data includes details such as artist names, artwork titles, years, ObjectIDs, artwork URLs, and thumbnail image URLs. The files generated through this script is used as a base data which is saved in "Collection_Pages".

- __`extend_artworks_data.py`__ -  This script  retrieves artwork data from JSON files in the "Collection_Pages" directory. It asynchronously processes the data using concurrent threading to extract additional details and artist profiles from the Museum of Modern Art website. The script saves the extended data into new JSON files in the "ExtendedCollection" directory.

- __`move_broken_pages.py`__ - A data validation tool that examines JSON files located in the "ExtendedCollection" directory. It checks whether each JSON file contains a list of objects, and within each object, whether both "Details" and "Profile" fields are present. If any object within a JSON file is found to be missing either of these fields, the script moves that JSON file to the "PagesBroken" directory for further inspection or fixing.

- __`fix_broken_data.py`__ -  Fixes broken artist profile links and missing details in JSON data files stored in the "PagesBroken" directory. After extracting the missing data, it updates the JSON files in the "PagesFixed" directory with the corrected profile URLs and details. The final output ensures that the JSON data files have accurate and complete information about the artists available on the MoMA website.

- __`build_artworks_dataset.py`__ - It consolidates JSON data from two directories, "ExtendedCollection" and "PagesFixed." Then, it loads the JSON data from all files in the "ExtendedCollection" directory and combines it into a single list. After that, it removes all JSON files from the "PagesFixed" directory. Finally, the script saves the merged JSON data into a new file named "artworks.json" in the current script directory.

- __`sort_artworks.py`__ - Performs data processing on artworks by sorting them based on their `ObjectID` and saves the sorted data to a new JSON file.

- __`convert_to_csv.py`__ - It transforms nested JSON data, specifically representing artworks, into a flattened CSV format. By recursively flattening nested dictionaries within each artwork, the script creates a structured CSV file that allows for easier handling and analysis of the data in a tabular format.


__Artists__ - Run the following scripts in order.

- __`fetch_artists.py`__ -  Retrieves artist profile links from MoMA's website. It saves the links into individual JSON files, with each file containing a list of profile URLs and their corresponding IDs.
- __`extend_artists_data.py`__ - Extends artist data from MoMA's website using previously saved profile links. It fetches profile links from JSON files in the "SeparatePages" directory and extracts additional detailsThe extended data is then saved into separate JSON files in the "ExtendedCollection" directory.
- __`merge_all_artists.py`__ - Merges multiple JSON files containing extended artist data into a single file. It takes as input an "ExtendedCollection" directory where individual JSON files with artist information are stored. The script reads each JSON file, extracts its data, and appends it to the "artists.json" file in the root directory.
