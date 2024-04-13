
from __future__ import annotations

import os
from typing import List, Dict

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from classes.config import CONFIG
from libs.args import process_arguments
from libs.logging.logger import Logging
from libs.logging.wrappers import PropertyWrapper

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_extension('adblock.crx')
options.add_argument('--start-maximized')
options.add_argument('--blink-settings=imagesEnabled=false')  # block images
options.add_argument('--disable-extensions')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-gpu-blacklist')
options.add_argument('--use-gl')
options.add_argument("--disable-cookies")
options.add_argument('--disable-web-security')


def main() -> None:
    """Entry point of project."""
    arguments = process_arguments()
    load_dotenv(dotenv_path=os.path.join(".env", ".env"))

    Logging.prepare_to_output(
        prefix="<w>{0.datetime_now:%H:%M:%S} </w>",
        prefix_args=(PropertyWrapper(),),
    )

    Logging.echo(CONFIG.SETTING_EXAMPLE)
    Logging.echo("Hi Bro!")
    if arguments.test_string_argument is not None:
        Logging.echo("You passed -test_string_argument: '{message}'".format(message=arguments.test_string_argument))
    else:
        Logging.echo("You didn't pass -test_string_argument argument. It's not an error, it's only app logic :)")
    if arguments.test_bool_argument:
        Logging.echo("You passed -optional test_bool_argument as True")


def scrape_inews():
    url = 'https://inews.co.uk/category/news'

    # cat_url = 'https://inews.co.uk'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    Logging.echo(url)
    categories = []
    for category in soup.select('.inews__post-section__title > h2 > a'):
        category_url = category.get('href')
        category_name = category.text.strip()
        categories.append({'base_url': url + category_url, 'category_name': category_name})
    print(categories)


    classes = [
        'inews__post-jot__content-headline',
        'inews__post-hero__headline',
        'iinews__post-superhero__content'
    ]
    for category in categories:
        response = requests.get(category['base_url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        print(category['category_name'])
        # print(soup.find_all('div', {'class': 'inews__post'}))

        articles = []
        for class_name in classes:
            for article in soup.find_all('div', class_=class_name):
                link = article.find('a')

                if link:
                    article_url = link.get('href')
                    articles.append({'base_url': category['base_url'], 'url': article_url})
        print(articles)
    return articles

def scrape_svt():
    url = 'https://svt.se'

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    cookie_ok_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "root"] / div[2] / div / div[3] / button[3]')))
    cookie_ok_button.click()

    menu_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="nyh_a11y-primary-navigation-list"]/li[1]/a[2]'))
    )

    menu_item.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#nyh_a11y-primary-navigation-list > li:nth-child(1) > ul'))
    )

    menu_html = driver.page_source
    driver.quit()

    # response = requests.get(url)
    soup = BeautifulSoup(menu_html, 'html.parser')
    Logging.echo(url)
    # print(menu_html)
    categories = []
    for category in soup.select('.MenuCard__link___QTXVS'):
        if category.get('href').startswith('/nyheter/'):
            category_url = category.get('href')
            category_name = category.text.strip()
            categories.append({'base_url': url + category_url, 'category_name': category_name})
    print(categories)

    for category in categories:
        response = requests.get(category['base_url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        print(category['category_name'])

        articles = []
        for article in soup.find_all('a', class_='nyh_teaser__link'):
            article_url = article.get('href')
            articles.append({'base_url': category['base_url'], 'url': url + article_url})
        print(articles)
    return articles


def scrape_rtp() -> List:
    url = 'https://rtp.pt/noticias/'
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    cookie_ok_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button')))
    cookie_ok_button.click()

    menu_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'navbar-toggler'))
    )
    menu_item.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#nav-padder > ul:nth-child(2)'))
    )
    menu_html = driver.page_source
    # driver.quit()

    soup = BeautifulSoup(menu_html, 'html.parser')
    Logging.echo(url)
    # print(menu_html)
    categories = []
    menu_categories = soup.select('#nav-padder > ul:nth-child(2)')
    ul_element = menu_categories[0]
    for link in ul_element.find_all('a'):
        category_url = link.get('href')
        category_name = link.text.strip()
        if category_name == 'Vídeos':
            break
        categories.append({'category_name': category_name, 'base_url': category_url})
    print(categories)

    for category in categories:
        driver.get(category['base_url'])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#noticias > div.container.main-content.margin-top > div.row > div.sidebar_articles.col-12.col-lg-4.relative.bg-color.d-print-none.d-none.d-sm-none.d-lg-block > section'))
        )
        news_bar = driver.page_source
        soup = BeautifulSoup(news_bar, 'html.parser')
        articles = []
        for article in soup.find_all('article'):
            article_url = article.get('data-playlist-item-url')
            if article_url:
                articles.append({'base_url': category['base_url'], 'url': article_url})
        print(articles)
    driver.quit()
    return articles


def scrape_rtbf() -> List:
    url = 'https://www.rtbf.be/en-continu/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    Logging.echo(url)
    # print(soup.prettify())
    categories = []
    for cat in soup.find('ul', 'relative flex w-full select-none snap-x list-none flex-nowrap gap-6 overflow-x-auto lg:overflow-x-hidden sb-scroll-40 w-full gap-x-16').find_all('a', class_='outline-0'):
        category_url = cat.get('href').split('/')[-1]
        if category_url != 'en-continu':
            category_name = cat.find('span', class_='pointer-events-none').get_text(strip=True)
            categories.append({'category_name': category_name, 'base_url': url + category_url})
    print(categories)

    articles = []
    for category in categories:
        for article in soup.find_all('a', class_='stretched-link leading-[1.6rem] outline-none'):
            # link = article.find('a')

            # if link:
            article_url = article.get('href')
            articles.append({'base_url': category['base_url'], 'url': 'https://www.rtbf.be' + article_url})
    print(articles)


    return articles


if __name__ == "__main__":
    inews_articles = scrape_inews()
    svt_articles = scrape_svt()
    rtp_articles = scrape_rtp()
    rtbf_articles = scrape_rtbf()

    print('Scrapped iNews Articles:', len(inews_articles))
    print('Scrapped SVT Articles:', len(svt_articles))
    print('Scrapped RTP Articles:', len(rtp_articles))
    print('Scrapped RTBF Articles:', len(rtbf_articles))
