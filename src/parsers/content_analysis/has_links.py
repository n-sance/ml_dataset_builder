from bs4 import BeautifulSoup


def has_http_links(soup: BeautifulSoup) -> bool:
    anchor_tags = soup.find_all('a')
    links = [a['href'] for a in anchor_tags if 'href' in a.attrs]

    return bool([link for link in links if link.startswith('http://')])
