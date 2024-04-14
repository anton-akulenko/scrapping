from __future__ import annotations

from typing import List

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from classes.config import CONFIG
from libs.funcs import save, convert_publication_date, init_chrome
from libs.logging.logger import Logging


def scrape_24heures(url) -> List:
    driver = init_chrome()
    driver.get(url)
    cookie_ok_button = WebDriverWait(driver, 5).until(
        ec.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_ok_button.click()
    page_html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_html, "html.parser")
    Logging.echo(f"Scrapping...{url}")
    try:
        title = soup.find("span", "ContentHead_text__2MEnX").text
    except Exception as err:
        Logging.echo(f"{err}")
        title = None
    try:
        author = soup.find(
            "a", "ContentMetaInfo_authorlink__BYNhG link_underlinelink__K5Zr0"
        ).text
    except Exception as err:
        Logging.echo(f"{err}")
        author = None
    try:
        pub_date = soup.find(
            "time",
            "FullDateTime_root__K7FL2 ArticleContainer_content"
            "-width__FRl7F FullDateTime_-metainfo__e_tHp",
        ).get("datetime")
        datetime_f, readable_f = convert_publication_date(pub_date)
    except Exception as err:
        Logging.echo(f"{err}")
        datetime_f, readable_f = None, None
    try:
        paragraph_text = soup.find_all(
            "p",
            "ArticleParagraph_root__lhFZo ArticleContainer_content-width__FRl7F link_focus__0ZMwx"
            " link_externalicon-big__ZdPgo link_externalicon__qcwXs ArticleElement_article-element__q93eL",
        )
        if paragraph_text != []:
            content = " ".join([p.text for p in paragraph_text])
        else:
            content = soup.find(
                "h3",
                "ContentHead_lead____SsS link_regular__O0hk0"
                " link_externalicon-big__ZdPgo link_externalicon__qcwXs",
            ).text
    except Exception as err:
        Logging.echo(f"{err}")
        content = None
    filename = save(url, title, content, author, datetime_f, readable_f)
    Logging.echo(f"Data saved to file {filename}")


def scrape_breakinglatest(url) -> List:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    Logging.echo(f"Scrapping...{url}")
    try:
        title = soup.find("h1", "post-title single-post-title entry-title").text
    except Exception as err:
        Logging.echo(f"{err}")
        title = None

    try:
        author = soup.find(
            "a", "ContentMetaInfo_authorlink__BYNhG link_underlinelink__K5Zr0"
        ).text
    except Exception as err:
        Logging.echo(f"{err}")
        author = None

    try:
        pub_date = soup.find("time", "entry-date published").get("datetime")
        datetime_f, readable_f = convert_publication_date(pub_date)

    except Exception as err:
        Logging.echo(f"{err}")
        datetime_f, readable_f = None, None

    try:
        paragraph_text = soup.find(
            "div", class_="inner-post-entry entry-content"
        ).find_all("p")
        if paragraph_text != []:
            content = " ".join([p.text for p in paragraph_text])
        else:
            content = soup.find(
                "h3",
                "ContentHead_lead____SsS link_regular__O0hk0"
                " link_externalicon-big__ZdPgo link_externalicon__qcwXs",
            ).text
    except Exception as err:
        Logging.echo(f"{err}")
        content = None

    filename = save(url, title, content, author, datetime_f, readable_f)
    Logging.echo(f"Data saved to file {filename}")


def scrape_chiswickcalendar(url):
    driver = init_chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    Logging.echo(f"Scrapping...{url}")
    try:
        title = soup.find("h1", "post-title entry-title").text
    except Exception as err:
        Logging.echo(f"{err}")
        title = None

    try:
        author = soup.find("span", "entry-author-link").text
    except Exception as err:
        Logging.echo(f"{err}")
        author = None

    try:
        pub_date = soup.find("time", "date-container minor-meta updated").get(
            "datetime"
        )
        datetime_f, readable_f = convert_publication_date(pub_date)

    except Exception as err:
        Logging.echo(f"{err}")
        datetime_f, readable_f = None, None

    try:
        sections = []
        for h3 in soup.find_all("h3", class_=""):
            section = h3.text + "\n"
            next_elem = h3.find_next_sibling()
            while next_elem and next_elem.name != "h3":
                if (
                    next_elem.name == "p"
                    and "Read more" not in next_elem.text
                    and "Image above" not in next_elem.text
                ):
                    section += next_elem.text
                next_elem = next_elem.find_next_sibling()
            sections.append(section)
        content = "".join(sections)
    except Exception as err:
        Logging.echo(f"{err}")
        content = None

    filename = save(url, title, content, author, datetime_f, readable_f)
    Logging.echo(f"Data saved to file {filename}")


def scrape_corriere(url):
    driver = init_chrome()
    driver.get(url)
    cookie_ok_button = WebDriverWait(driver, 5).until(
        ec.element_to_be_clickable((By.ID, "privacy-cp-wall-accept"))
    )
    cookie_ok_button.click()
    page_html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_html, "html.parser")
    Logging.echo(f"Scrapping...{url}")
    try:
        title = soup.find("h1", "title-art-hp is-xmedium is-line-h-106 is-mr-b-20").text
    except Exception as err:
        Logging.echo(f"{err}")
        title = None

    try:
        author = soup.find("span", "writer is-mr-l-4").text
    except Exception as err:
        Logging.echo(f"{err}")
        author = None

    try:
        pub_date = soup.find("p", "is-last-update").get("datetime")
        if pub_date is None:
            pub_date = soup.find("p", "is-last-update").get("content")
        datetime_f, readable_f = convert_publication_date(pub_date)

    except Exception as err:
        Logging.echo(f"{err}")
        datetime_f, readable_f = None, None

    try:
        paragraph_text = soup.find_all("p", "chapter-paragraph")
        content = " ".join([p.text for p in paragraph_text])
    except Exception as err:
        Logging.echo(f"{err}")
        content = None
    filename = save(url, title, content, author, datetime_f, readable_f)
    Logging.echo(f"Data saved to file {filename}")


def main() -> None:
    Logging.echo("Starting scraping... Keep calm :)")
    [scrape_24heures(url) for url in CONFIG.URLS_24HEURES]
    [scrape_breakinglatest(url) for url in CONFIG.URLS_BREAKINGLATEST]
    [scrape_chiswickcalendar(url) for url in CONFIG.URLS_CHISWICKCALENDAR]
    [scrape_corriere(url) for url in CONFIG.URLS_CORRIERE]
    Logging.echo("Finished! Enjoy :)")


if __name__ == "__main__":
    main()
