from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pathlib import Path
import os
import time
import requests
from requests.exceptions import RequestException, ConnectionError


# open a session to get faster the image from wikipedia server
session = requests.Session()
# define collateral adjective index from the end of real columns table
ca_index_from_end = 0


def create_url_full_path(url_link):
    """
    Description: the function create url full path from relative path
    :param url_link: relative path
    :return: full path
    """
    base_url = 'https://en.wikipedia.org/'
    return urljoin(base_url, url_link)


def get_tables_from_wikipedia_page(url):
    """
    The function get the relevant tables from the url link
    :param url: Wikipedia page link
    :return: tables data
    """
    try:
        html_content = session.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table', {'class': 'wikitable'})
        if tables:
            return tables
        else:
            raise ValueError(f"The link doesn't contain any table")
    except ConnectionError:
        raise ConnectionError(f"Unable to connect to the internet or the server of {url}")
    except RequestException as e:
        raise ValueError(f"The link or the request to URL {url} not valid: {e}")


def tmp_folder():
    """
    Description: create tmp folder in the project folder, if doesn't exist
    :return: tmp folder path
    """
    tmp_dir = Path.cwd() / 'tmp'
    tmp_dir.mkdir(exist_ok=True)
    return tmp_dir


def get_local_image_path(animal):
    """
    Description: create the local path to animal picture
    :param animal: animal name
    :return: local animal picture path
    """
    img_name = animal + '.jpg'
    return tmp_folder() / img_name


def download_picture(url_link, animal):
    """
    Description: download a picture from wikipedia link
    :param url_link: url link
    :param animal: animal name
    """
    img_path = get_local_image_path(animal)
    if img_path.exists():
        return

    try:
        res = session.get(url_link)
        animal_soup = BeautifulSoup(res.text, 'html.parser')

        img_tag = animal_soup.find("table", class_="infobox").find("img") if animal_soup.find("table", class_="infobox") else None
        if not img_tag:
            content = animal_soup.find("div", id="mw-content-text")
            img_tag = content.find("img") if content else None
        img_url = 'https:' + img_tag['src'] if img_tag else None

        if img_url:
            for attempt in range(10):
                img_data = session.get(img_url, timeout=5).content
                with open(img_path, "wb") as file:
                    file.write(img_data)
                if os.path.getsize(img_path) > 2048:
                    break
                else:
                    os.remove(img_path)
                time.sleep(0.5)
    except:
        pass  # the program will continue if one or more pictures didn't download


def get_table_headers(table):
    """
    Description: Get headers from the table, raise error if there aren't headers
    :param table: current table from wikipedia
    :return list of the headers
    """
    headers = [th.text.strip() for th in table.find_all('th')]
    if not headers:
        raise ValueError("No headers found in the table")
    return headers


def get_table_rows(table):
    """
    Description: get rows, excluding the header
    :param table: the wikipedia table
    :return the rows without the first one
    """
    return table.find_all('tr')[1:]  # Skip the first row


def get_collateral_adjective(row, ca_index_from_end, ca_index):
    """
    Description: get the collateral adjective from a row
    :param row: one row in the table
    :param ca_index_from_end: collateral adjective index from the end of real columns table
    :param ca_index: the index of 'ca' for the current table
    :return the collateral adjective of the row
    """
    try:
        return row.find_all('td')[ca_index_from_end].text.strip() if ca_index < len(row.find_all('td')) + 1 else ''
    except:
        return None

def wanted_columns(headers):
    """
    Description: The function gets table headers and returns dictionary of wanted columns and their indices
    There are two tables in the Wikipedia page, with different column value,
    I adapt the relevant wanted columns per table
    :param headers: list of the table headers
    :return: return dictionary of wanted name column with their index
    """
    base_columns = ["Young", "Female", "Male"]
    if "Animal" in headers:
        base_columns.append("Animal")
    if "Trivial name" in headers:
        base_columns.append("Trivial name")
    return {column: headers.index(column) for column in base_columns}


def get_table_indices(headers, collateral_adjective_str):
    """
    Description: This function finds the indices of the wanted columns and the collateral adjective column
    :param headers: list of the table headers
    :param collateral_adjective_str string of the wanted column header
    :returns: return dictionary of wanted name column with their index, index of the collateral adjective column - from start and end
    """
    global ca_index_from_end
    wanted_columns_indices = wanted_columns(headers)

    # the index of the collateral adjective column
    ca_index = next(idx for idx, ca in enumerate(headers) if ca == collateral_adjective_str)

    ca_index_from_end -= 1
    return wanted_columns_indices, ca_index, ca_index_from_end
