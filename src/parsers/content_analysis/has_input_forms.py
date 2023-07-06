from bs4 import BeautifulSoup


def check_input_forms(soup: BeautifulSoup) -> tuple:
    input_elements = soup.find_all('input')
    password_inputs = soup.find_all('input', {'type': 'password'})
    base_text_inputs = soup.find_all('textarea')

    return bool(input_elements), bool(password_inputs), bool(base_text_inputs)
