"""
Description: this file contain the entities classes
Two classes:
1. Collateral Adjective class, include his name and Animals objects list
2. Animal class, include his name and their picture local link - if exist
"""


class Animal:
    def __init__(self, name, image=None):
        self.name = name
        self.local_image_link = image


class CollateralAdjective:
    def __init__(self, name):
        self.name = name
        self.animals = []
