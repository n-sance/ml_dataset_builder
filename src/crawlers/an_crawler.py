import os
import time
from urllib.parse import urlparse, urljoin
from selenium.webdriver.common.by import By
import requests
import uuid
import base64
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from src.common.log_management import log

requests.packages.urllib3.disable_warnings()

options = Options()
options.add_argument("--disable-web-security")
options.add_argument("--ignore-certificate-errors")
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--headless")
options.add_argument("--window-size=1440,900")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.3')

service = Service(service_args=['--verbose', '--log-path=selenium_log.log'])

driver = webdriver.Chrome(options=options, service=service)
driver.set_page_load_timeout(30)


def save_web_page(url: str, save_folder: str, screenshot: bool):
    # Создаем папку для сохранения ресурсов, если она не существует
    os.makedirs(save_folder, exist_ok=True)

    # Указываем путь к драйверу Chrome и сервису
    driver = webdriver.Chrome(options=options)

    try:
        # Загружаем веб-страницу
        time.sleep(1)
        driver.get(url)

        with open(os.path.join(save_folder, 'url.txt'), 'w') as f:
            f.write(url + '\n')

        if screenshot is True:
            original_size = driver.get_window_size()
            required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(required_width, required_height)
            # driver.save_screenshot(path)  # has scrollbar
            driver.find_element(By.TAG_NAME, 'body').screenshot(os.path.join(save_folder, "and_full_page_screenshot.png"))  # avoids scrollbar
            driver.set_window_size(original_size['width'], original_size['height'])


        # Получаем HTML-код страницы после выполнения JavaScript
        html = driver.page_source

        # Сохраняем HTML-код
        html_filename = 'index.html'
        html_save_path = os.path.join(save_folder, html_filename)
        with open(html_save_path, 'w', encoding='utf-8') as file:
            file.write(html)

        # Получаем все теги <img> и сохраняем изображения
        img_elements = driver.find_elements(By.TAG_NAME, 'img')
        for img_element in img_elements:
            img_url = img_element.get_attribute('src')
            abs_img_url = urljoin(url, img_url)
            save_resource(abs_img_url, save_folder)

        # Получаем все теги <link> с rel="stylesheet" и сохраняем CSS стили
        link_elements = driver.find_elements(By.CSS_SELECTOR, 'link[rel="stylesheet"]')
        for link_element in link_elements:
            css_url = link_element.get_attribute('href')
            abs_css_url = urljoin(url, css_url)
            save_resource(abs_css_url, save_folder)

        # Получаем все теги <script> и сохраняем скрипты
        script_elements = driver.find_elements(By.TAG_NAME, 'script')
        for script_element in script_elements:
            script_url = script_element.get_attribute('src')
            if script_url:
                abs_script_url = urljoin(url, script_url)
                save_resource(abs_script_url, save_folder)

        return html_save_path
    except Exception as err:
        log.error(f'Error saving {url}: {err}')
    finally:
        driver.quit()


def save_resource(url, save_folder):
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        filename = os.path.basename(urlparse(url).path) or generate_random_filename()
        save_path = os.path.join(save_folder, filename)

        # Проверяем, является ли путь файлом
        if os.path.isfile(save_path):
            # Если файл с таким именем уже существует, добавляем уникальный суффикс
            filename = get_unique_filename(filename)
            save_path = os.path.join(save_folder, filename)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return save_path

    except requests.exceptions.RequestException as e:
        log.error(f"Error downloading: {url}: {e}")
        return None


def generate_random_filename(extension=''):
    random_filename = str(uuid.uuid4())
    if extension:
        random_filename = 'undef_' + random_filename + '.' + extension.strip('.')
    return random_filename[:12]


def get_unique_filename(filename):
    # Получаем имя файла без расширения
    name, ext = os.path.splitext(filename)

    # Генерируем уникальное имя файла с добавлением суффикса
    suffix = 1
    while os.path.isfile(filename):
        filename = f"{name}_{suffix}{ext}"
        suffix += 1

    return filename

if __name__ == '__main__':
    save_web_page('https://www.sooninn.com.tw/wp-content/themes/seotheme/wordpr/dhl-rd354/index.html', 'here', screenshot=True)