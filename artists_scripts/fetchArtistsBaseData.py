import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

headers = {
    'Host': 'www.moma.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.moma.org/artists/34',
    'Connection': 'keep-alive'
}

def fetch_url(url):
    response = requests.get(url, headers=headers)
    return response.text

def parse_page_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = 'https://www.moma.org'
    links = [base_url + a['href'] for a in soup.find_all('a', class_='link/enable:children')]
    return links

def fetch_and_save_links(page_num):
    save_file = f"../Files/Artists/SeparatePages/{page_num}_artist_links.json"
    if os.path.exists(save_file):
        print(f"Skipping page {page_num}, file already exists.")
        return

    url = f"https://www.moma.org/artists/?q=&page={page_num}"
    html_content = fetch_url(url)
    links = parse_page_content(html_content)

    formatted_links = [{'page': link, 'ID': int(link.split('/')[-1])} for link in links]

    with open(save_file, 'w') as file:
        json.dump(formatted_links, file, indent=2)
    print(f"Page {page_num} scraped and saved.")

def main(num_pages):
    os.makedirs("../Files/Artists/SeparatePages/", exist_ok=True)
    with ThreadPoolExecutor() as executor:
        executor.map(fetch_and_save_links, range(1, num_pages + 1))

if __name__ == "__main__":
    num_pages = 1
    main(num_pages)
