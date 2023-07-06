from typing import List
from bs4 import BeautifulSoup


def extract_text(soup: BeautifulSoup) -> List[str]:
    text = soup.get_text()
    text = text.split('\n')
    text = [line for line in text if line.strip()]

    return text
