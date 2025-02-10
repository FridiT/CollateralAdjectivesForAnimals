import re


def split_values(text):
    """
    Description: the function split the cell by , or \n
    :param text: content of one cell in the table as a string
    :return: list of the relevant term from the text
    """
    if text == '—':
        return []
    words = [word.strip() for word in re.split(r'[\n,;/]|\s*\bor\b\s*', text) if word.strip()]
    words = [word.capitalize() for word in words]
    return [word for word in words if word not in {'Other', 'Others'}]


def clean_values(text):
    """
    Description: the function clean the terms from parentheses and description
    :param text: content of one cell in the table
    :return: string of the text without not necessary content
    """
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    return re.sub(r'\b(family of|group of|also see|see)\b.*?([,\n]|$)', r'\2', text, flags=re.IGNORECASE)

