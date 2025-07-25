from os import PathLike, walk, path
from itertools import chain
from pathlib import Path

import requests
from django.conf import settings

from bs4 import BeautifulSoup


def make_book_dict(path: PathLike, relative_path_from: PathLike, xml_str : str) -> dict:
    """Extracts some information from the book xml string 
    and its file path and puts it into a dict."""

    def maybe_str(maybe) -> str | None:
        if maybe is not None:
            return maybe.string

    soup = BeautifulSoup(xml_str, 'xml')

    tiltle = maybe_str(soup.find('title'))
    author = maybe_str(soup.find('author'))
    editor = maybe_str(soup.find('editor', attrs={'role': None}))
    translator = maybe_str(soup.find('editor', attrs={'role': 'translator'}))
    maybe_imprint = soup.find('imprint')
    if maybe_imprint:
        date = maybe_str(maybe_imprint.find('date'))
    else:
        date = maybe_str(soup.find('date'))

    path_obj = Path(path)
    directory_path = str(path_obj.relative_to(relative_path_from).parent)
    file_name = path_obj.stem.replace('.', '-')

    for key, value in settings.LANG_VALUES.items():
        if key in file_name:
            lang = value
            break
    else: 
        lang = None

    return {
        'title': tiltle,
        'author': author,
        'editor': editor,
        'translator': translator,
        'date': date,
        'directory_path': directory_path,
        'file_name': file_name,
        'language': lang,
    }


def generate_file_names(dir_path: str) -> list[str]:
    """Takes path to the data directory of a repo,
    returns an unorganized list of book file paths, 
    excluding any __cts__.xml and .json files."""

    walked = list(walk(dir_path))

    def join_paths(walked_tuple: tuple[str, list[str], list[str]]) -> list[str]:
        root, _, files = walked_tuple
        return list(map(lambda el: path.join(root, el), files))
    
    file_paths_lists = list(map(join_paths, walked))
    
    file_paths = list(chain(*file_paths_lists))

    cleaned_up_paths = list(filter(
        lambda el: 
            not ('__cts__.xml' in el) and 
            not ('.json' in el), 
        file_paths))
    
    return cleaned_up_paths


def send_to_convert(hosting: str, data: bytes, ingore_non_200_responses=False):
    """Sends an XML document to be converted to HTML on the TeiGarage hosting,
    according to their API."""

    address = hosting + '/ege-webservice//Conversions/TEI%3Atext%3Axml/xhtml%3Aapplication%3Axhtml%2Bxml/conversion?properties=<conversions><conversion index="0"><property id="oxgarage.getImages">true</property><property id="oxgarage.getOnlineImages">true</property><property id="oxgarage.lang">en</property><property id="oxgarage.textOnly">false</property><property id="pl.psnc.dl.ege.tei.profileNames">default</property></conversion></conversions>'
    response = requests.post(address, files={'upload': data})

    if not ingore_non_200_responses and response.status_code != 200:
        raise RuntimeError('Something went wrong on the TeiGarage side.\n'
                          f' Response status code: {response.status_code}.')

    return response.text
