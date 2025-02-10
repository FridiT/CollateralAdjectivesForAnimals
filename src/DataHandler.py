from src.DataClasses import Animal, CollateralAdjective


def add_animal_to_data(data, collateral_adjective, animal_name, image_url=None):
    """
    Description: the function add to the main data structure animals
    and their picture link according to their collateral adjective
    :param data: dictionary with collateral adjective with the animals that belong him
    :param collateral_adjective: string of collateral adjective the animal belong to
    :param animal_name: animal name as a string
    :param image_url: local path to the animal picture or None -
    in case of the animal doesn't has picture or didn't success to valid download
    """
    if collateral_adjective not in data:
        data[collateral_adjective] = CollateralAdjective(CollateralAdjective)
    if animal_name not in {animal.name for animal in data[collateral_adjective].animals}:
        data[collateral_adjective].animals.append(Animal(animal_name, image_url))


def get_sorted_data(data):
    """
    Description: sort the collateral_adjective and the animals
    :param data: data: dictionary with collateral adjective with the animals that belong him
    :return: sorted data dictionary
    """
    sorted_data = {}

    for key in sorted(data):
        sorted_animals = sorted(data[key].animals, key=lambda animal: animal.name)

        collateral = CollateralAdjective(name=key)
        collateral.animals = sorted_animals
        sorted_data[key] = collateral

    return sorted_data
