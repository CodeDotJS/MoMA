<h1 align="center"><img src="media/moma.png"></h1>

## Description

MoMA Artworks Scraper and Dataset Builder is designed to collect and organize data about artworks and artists from the Museum of Modern Art (MoMA). This project gathers essential details about Artworks and Artists. It then saves the collected data in both JSON and CSV formats, making it easy to use for further analysis and research.

__Artworks Data__

The [artworks.json](artworks.json) file contains a vast collection of __100,110 artworks__ from the Museum of Modern Art (MoMA). Each artwork entry is represented as a JSON object with comprehensive details, including the artist's name, title, year, medium, dimensions, publisher, edition, credit, object number, copyright, portfolio, department, and more.

__Example__

```JSON
{
    "Artist": "Frida Kahlo",
    "Title": "My Grandparents, My Parents, and I (Family Tree)",
    "Year": "1936",
    "ObjectID": 78784,
    "Work": "https://www.moma.org/collection/works/78784",
    "Thumbnail": "https://www.moma.org/media/W1siZiIsIjQ3N...M2UiXV0.jpg?sha=c411357c15216300",
    "Details": {
        "Medium": "Oil and tempera on zinc",
        "Dimensions": "12 1/8 x 13 5/8\" (30.7 x 34.5 cm)",
        "Credit": "Gift of Allan Roos, M. D., and B. Mathieu Roos",
        "Object number": "102.1976",
        "Copyright": "\u00a9 2023 Banco de M\u00e9xico Diego Rivera Frida Kahlo Museums Trust, Mexico, D.F. / Artists Rights Society (ARS), New York",
        "Department": "Painting and Sculpture"
    },
    "Profile": "https://www.moma.org/artists/2963"
}
 ```

__Artists Data__

The [artists.json](artists.json) file is a dataset containing information about various artists represented in the Museum of Modern Art. With __27,385 entries__, each artist's data is represented as a JSON object, providing details such as the artist's page URL, ID, name, and bio. Additionally, the dataset includes extended details (if available on MoMA's site) about each artist, including an introduction, Wikidata ID, nationality, gender, roles, alternative names, Ulan ID, and more.

__Example__

```JSON
{
    "page": "https://www.moma.org/artists/2963",
    "ID": 2963,
    "name": "Frida Kahlo",
    "bio": "Mexican, 1907–1954",
    "details": {
        "Introduction": "Mexican fantasy painter known as much for her turbulent personal life as her fanciful self-portraits. ... Her work received notoriety in the 1970's, becoming popular with feminist art historians and Latin Americans living in the United States.",
        "Wikidata": "Q5588",
        "Nationality": "Mexican",
        "Gender": "Female",
        "Roles": "Artist, Painter",
        "Names": "Frida Kahlo, Frida Kahlo de Rivera, Frida Rivera, De Rivera Kahlo.. Frida Rivera-Kahlo",
        "Ulan": "500030701"
    }
}

```
## Motivation

The primary motivation behind this project is to build an extensive dataset of MoMA's artists and art collection and create an accessible API. As the original API is restricted to MoMA staff and partners, this project seeks to provide a publicly available alternative.

## Features

- Uses concurrent/asynchronous programming for faster data collection and processing.
- Gathers Artwork information from  more than __100k pages__ in MoMA's collection.
- Gathers Artist information from  more than __27k pages__ in MoMA's collection.
- Saves and extends the artwork/artists data in JSON format for each page.
- Sorts and converts the collected data to CSV for easier analysis.

## Build

Building datasets for both Artists and Artworks requires different scripts. The complete steps are mentioned __[here](docs/workground.md)__.

## Contributing

If you're interested in contributing, you can start by forking the repository. After that, create a separate branch to work on your changes, and once you're done, submit a pull request with your modifications.

## Related

- [MoMA API]() - Flask-based API for MoMA Artworks/Artists dataset. Explore MoMA's art collection and artist details with ease.

## License

MIT License
