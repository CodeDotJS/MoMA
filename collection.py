import asyncio
import json
import aiohttp
import unicodedata
from bs4 import BeautifulSoup
import os

headers = {
    'Host': 'www.moma.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.moma.org/artists/34',
    'Connection': 'keep-alive'
}

base_url = "https://www.moma.org/collection/?=undefined&page={}&direction=fwd"
image_base_url = "https://www.moma.org"

all_data = {}

start = input("Get data from page: ")
end = input("Get data till page: ")


async def fetch_page(session, page_number):
    url = base_url.format(page_number)
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                link_elements = soup.find_all(class_='grid-item__link')

                page_data = []
                for index, element in enumerate(link_elements, 1):
                    artist = ''
                    title = ''
                    year = ''
                    image_url = ''
                    item_url = "https://www.moma.org" + element.get('href').split('?')[0] if element.get('href') else ''

                    span_elements = element.find_all(class_='work--in-list__caption__text')
                    if len(span_elements) > 0:
                        artist = normalize_text(span_elements[0].text.strip())
                    if len(span_elements) > 1:
                        title = normalize_text(span_elements[1].text.strip())
                    if len(span_elements) > 2:
                        year = normalize_text(span_elements[2].text.strip()).replace('\u2013', '-')

                    image_element = element.find('img', class_='picture__img--static')
                    if image_element:
                        image_path = image_element.get('src')
                        image_url = image_base_url + image_path if image_path else ''

                    data = {
                        'Artist': artist,
                        'Title': title,
                        'Year': year,
                        'ObjectID': item_url.rsplit('/', 1)[-1],
                        'Work': item_url,
                        'Thumbnail': image_url
                    }
                    page_data.append(data)

                page_key = "Page_{}".format(page_number)
                all_data[page_key] = page_data
                print(f"Extracted data from Page {page_number}")
            else:
                print(f"Failed to fetch Page {page_number}. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred while fetching Page {page_number}: {str(e)}")


def normalize_text(text):
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in normalized if not unicodedata.combining(c))


async def scrape_pages():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_number in range(int(start), int(end) + 1):
            task = asyncio.ensure_future(fetch_page(session, page_number))
            tasks.append(task)
            if len(tasks) == 25:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(scrape_pages())

async def save_page_data_as_json(page_number, data):
    filename = f"{page_number}_moma_collection.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

async def save_all_data_as_json():
    for page_number, data in all_data.items():
        await save_page_data_as_json(page_number, data)

loop.run_until_complete(save_all_data_as_json())

complete_data = {}
for page_number in range(int(start), int(end) + 1):
    filename = f"Page_{page_number}_moma_collection.json"
    with open(filename, 'r') as json_file:
        page_data = json.load(json_file)
        complete_data.update({f"{page_number}": page_data})

with open('collection.json', 'w') as json_file:
    json.dump(complete_data, json_file, indent=4)
print("\nData merged and saved in collection.json")

for page_number in range(int(start), int(end) + 1):
    filename = f"Page_{page_number}_moma_collection.json"
    os.remove(filename)
print("Removed base pages!")
