import requests
from bs4 import BeautifulSoup
from pathlib import Path

from common.rest_management import smart_request
from common.files_management import open_saved_webpage, write_to_file
from parsers.content_analysis.has_links import has_http_links
from parsers.content_analysis.has_input_forms import check_input_forms
from parsers.content_analysis.extract_text import extract_text


def analyze_page_content(scheme: str, netloc: str, path_n_params: str, mode: str = 'online', storage: Path = None,
                         store_text: bool = False):
    try:
        if mode == 'online':
            r = smart_request(netloc, scheme=scheme, path_n_params=path_n_params)
            soup_content = BeautifulSoup(r.content, 'html.parser')
        else:
            r = open_saved_webpage(storage / (netloc + '.html'))
            soup_content = BeautifulSoup(r, 'html.parser')

        if store_text is True:
            txt = extract_text(soup_content)
            write_to_file(storage / (netloc + '.txt'), txt)

        has_links = has_http_links(soup_content)
        has_inputs, has_pwds, has_textareas = check_input_forms(soup_content)

    except requests.RequestException as err:
        print(f'Failed to retrieve data for {scheme + netloc + path_n_params}: {err}')
        return [None] * 4

    return has_links, has_inputs, has_pwds, has_textareas
