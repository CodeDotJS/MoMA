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
    url = artist_data["Work"]
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        details_element = soup.find(id="caption")
        if details_element:
            details = {}
            dt_elements = details_element.find_all("dt")
            dd_elements = details_element.find_all("dd")

            for dt, dd in zip(dt_elements, dd_elements):
                key = dt.get_text().strip()
                value = dd.get_text().strip()
                details[key] = value

            artist_data["Details"] = details

            profile_href = soup.select_one('.typography.typography\\/underline\\:disable a[href]')
            if not profile_href:
                profile_href = soup.find(class_="typography typography\\/underline:disable").a

            if profile_href:
                href = profile_href["href"]
                absolute_url = urljoin("https://www.moma.org", href)
                with lock:
                    artist_data["Profile"] = absolute_url

def process_json_file(file_path, output_directory):
    with open(file_path) as json_file:
        data = json.load(json_file)

    lock = threading.Lock()

    total_artists = len(data)
    max_workers = min(total_artists, os.cpu_count() * 5)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for artist_data in data:
            futures.append(executor.submit(scrape_artist_data, artist_data, total_artists, lock))

        with tqdm(total=total_artists, desc=f"Processing file: {file_path}", ncols=80) as pbar:
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"\nError scraping artists: {str(e)}")

                pbar.update(1)

    output_file = f"extended_{os.path.basename(file_path)}"
    output_path = os.path.join(output_directory, output_file)
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

directory = "Collection_Pages/"
output_directory = "ExtendedCollection/"

os.makedirs(output_directory, exist_ok=True)

start_page = int(input("Enter the starting page number to scrape from: "))
end_page = int(input("Enter the end page number to stop scraping: "))

for page_number in range(start_page, end_page + 1):
    filename = f"{page_number}_MoMA.json"
    file_path = os.path.join(directory, filename)
    output_file = f"extended_{filename}"
    output_path = os.path.join(output_directory, output_file)

    if os.path.isfile(output_path):
        print(f"Page {page_number} has already been scraped. Skipping...")
        continue

    if os.path.isfile(file_path):
        process_json_file(file_path, output_directory)
    else:
        print(f"File {filename} does not exist.")
