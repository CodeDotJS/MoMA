import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures
import threading
import os
from tqdm import tqdm

headers = {
    'Host': 'www.moma.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.moma.org/artists/34',
    'Connection': 'keep-alive'
}

def scrape_artist_data(artist_data, total_artists, lock):
    if "Details" not in artist_data or "Profile" not in artist_data:
        url = artist_data["Work"]
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            details_element = soup.find(id="caption")
            if details_element and "Details" not in artist_data:
                details = {}
                dt_elements = details_element.find_all("dt")
                dd_elements = details_element.find_all("dd")

                for dt, dd in zip(dt_elements, dd_elements):
                    key = dt.get_text().strip()
                    value = dd.get_text().strip()
                    details[key] = value

                artist_data["Details"] = details

            if "Profile" not in artist_data:
                profile_href = soup.select_one('.typography.typography\\/underline\\:disable a[href]')
                if not profile_href:
                    profile_href = soup.find(class_="typography typography\\/underline:disable").a

                if profile_href:
                    href = profile_href["href"]
                    absolute_url = urljoin("https://www.moma.org", href)
                    with lock:
                        artist_data["Profile"] = absolute_url

def process_json_file(input_file_path, output_file_path, total_artists):
    with open(input_file_path) as json_file:
        data = json.load(json_file)

    lock = threading.Lock()

    max_workers = min(total_artists, os.cpu_count() * 5)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for artist_data in data:
            futures.append(executor.submit(scrape_artist_data, artist_data, total_artists, lock))

        with tqdm(total=total_artists, desc=f"Processing file: {input_file_path}", ncols=80) as pbar:
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"\nError scraping artists: {str(e)}")

                pbar.update(1)

    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def process_all_files(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, filename)
            total_artists = 0
            with open(input_file_path) as json_file:
                data = json.load(json_file)
                total_artists = len(data)

            process_json_file(input_file_path, output_file_path, total_artists)

if __name__ == "__main__":
    input_directory = "../Files/PagesBroken/"
    output_directory = "../Files/PagesFixed/"

    process_all_files(input_directory, output_directory)
