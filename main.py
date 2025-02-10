from concurrent.futures import ThreadPoolExecutor
from src.GenerateHTML import GenerateHTML
from src.DataHandler import *
from src.utils import *
from src.WikiHandler import *


collateral_adjective_str = "Collateral adjective"


def run():
    data = {}
    tables = get_tables_from_wikipedia_page('https://en.wikipedia.org/wiki/List_of_animal_names')
    with ThreadPoolExecutor(max_workers=7) as executor:

        for table in tables:
            headers = get_table_headers(table)
            wanted_columns_indices, ca_index, ca_index_from_end = get_table_indices(headers, collateral_adjective_str)

            rows = get_table_rows(table)

            for row in rows:
                collateral_adjective = get_collateral_adjective(row, ca_index_from_end, ca_index)  # find the collateral adjective of the row
                if not collateral_adjective:
                    continue  # Skip row without collateral adjective

                ca_list = split_values(clean_values(collateral_adjective))  # split the cell in case of different collateral adjective in the cell

                for idx, td in enumerate(row.find_all('td')):  # extract all values from the row cross wanted columns
                    if idx in wanted_columns_indices.values() and ca_list:  # work just with the wanted columns
                        cell_list = split_values(clean_values(td.text.strip()))
                        for ca in ca_list:
                            for animal in cell_list:
                                link = td.find('a') if animal in str(td.find('a')) else None
                                img_path = get_local_image_path(animal) if link else None
                                add_animal_to_data(data, ca, animal, img_path)
                                if link:
                                   executor.submit(download_picture, create_url_full_path(link.get('href')), animal)

    GenerateHTML.generate_html(get_sorted_data(data))  # generate the HTML after all the data processing is done


if __name__ == '__main__':
    run()
