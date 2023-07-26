import os
import json
import requests
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm

headers = {
    'Host': 'www.moma.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'getty-record-should-start-opened=true; wikipedia-entry-should-start-opened=false; viewedCookieBanner=true; global=MTY4OTkyNDg2MHxOd3dBTkZOWFZqWXpSa3RLUlVOSFExWlJXazgzVGs5VU0wOHlRVWxYVGxoTFQwUkJSVTFUVGtkVlJreEJOVUZPTmtoRFNrOWFTRUU9fJ7F9ljtKT4IampbL5RPDKLDAvorL-v_icsF6eE7unUF; cf_clearance=nnprQ_A70YbNppmewYhFFUvvpOp7sJaH4ckibmRqGFo-1689923373-0-0.2.1689923373; _gorilla_csrf=MTY4OTg5MDExMnxJbkZyVkdNMVNVSjNlRmwzYnl0QmRXRldka1E1TW1WallrdFNiRmN4Umpjd0sxQkVkMjB4ZHpaNk1uTTlJZ289fCafckxXyuUDzwMqDe4L3nf-ulwHf_-rshoZt8pA-lZP; sessionHighlightColor=5',
}

def fetch(url, max_retries=3, retry_delay=1):
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            return response.text
        except requests.RequestException as e:
            if attempt < max_retries:
                print(f"Retry attempt {attempt + 1}/{max_retries} for URL: {url}")
                time.sleep(retry_delay)
            else:
                raise e

def process_artist(item):
    page_url = item["page"]
    artist_id = item["ID"]
    html = fetch(page_url)

    soup = BeautifulSoup(html, "html.parser")

    first_section = soup.find('section')
    h1_element = first_section.find('h1')
    h2_element = first_section.find('h2')

    name_span = h1_element.find('span', class_='layout/block') if h1_element else None
    bio_span = h2_element.find('span', class_='layout/block balance-text') if h2_element else None
    name = name_span.get_text(strip=True) if name_span else None
    bio = bio_span.get_text(strip=True) if bio_span else None

    details = {}
    dt_elements = soup.find_all('dt')
    for dt_element in dt_elements:
        key = dt_element.get_text(strip=True)
        value = dt_element.find_next('dd').get_text(strip=True)
        details[key] = value

    extended_item = {
        "page": page_url,
        "ID": artist_id,
        "name": name,
        "bio": bio,
        "details": details if details else None
    }

    return extended_item


def process_artists(data):
    extended_data = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_artist, item) for item in data]
        for future in tqdm(futures, total=len(data), desc="Processing artists"):
            extended_data.append(future.result())
    return extended_data

def scrape_and_save_extended_json(input_folder, output_folder, start_page=1, end_page=None):
    files_processed = set()

    try:
        for collection_filename in os.listdir(output_folder):
            if collection_filename.endswith("_extended.json"):
                files_processed.add(collection_filename.replace("_extended.json", ".json"))

        files_to_process = sorted([filename for filename in os.listdir(input_folder) if filename.endswith(".json")])

        for filename in files_to_process:
            page_number = int(filename.split("_")[0])

            if start_page <= page_number and (end_page is None or page_number <= end_page):
                if filename not in files_processed:
                    with open(os.path.join(input_folder, filename), "r") as file:
                        data = json.load(file)
                    print(f"Processing file: {filename}")

                    extended_data = process_artists(data)

                    os.makedirs(output_folder, exist_ok=True)

                    extended_filename = f"{filename[:-5]}_extended.json"

                    with open(os.path.join(output_folder, extended_filename), "w") as outfile:
                        json.dump(extended_data, outfile, indent=2)

                    files_processed.add(filename)
                else:
                    print(f"Skipped file: {filename} (Page number: {page_number})")

    except (requests.RequestException, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"An error occurred during processing: {e}")

    except KeyboardInterrupt:
        print("Process interrupted by the user.")
        return

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    input_folder_path = "../Files/Artists/SeparatePages"
    output_folder_path = "../Files/Artists/ExtendedCollection"
    start_page = int(input("Enter the starting page number to scrape from: "))
    end_page = int(input("Enter the ending page number to scrape until (press Enter to scrape all pages): ") or 0)

    scrape_and_save_extended_json(input_folder_path, output_folder_path, start_page, end_page)

if __name__ == "__main__":
    main()
