from __future__ import annotations

from typing import List

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from classes.config import CONFIG
from libs.funcs import init_Chrome, save_articles
from libs.logging.logger import Logging


def scrape_inews(url) -> List:
    classes = [
        "inews__post-jot__content-headline",
        "inews__post-hero__headline",
        "iinews__post-superhero__content",
    ]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    Logging.echo(f"Start collecting urls for {url}")
    categories = []
    for category in soup.select(".inews__post-section__title > h2 > a"):
        category_url = category.get("href")
        category_name = category.text.strip()
        categories.append(
            {"base_url": url + category_url, "category_name": category_name}
        )
    articles = []
    for category in categories:
        response = requests.get(category["base_url"])
        soup = BeautifulSoup(response.content, "html.parser")
        for class_name in classes:
            for article in soup.find_all("div", class_=class_name):
                link = article.find("a")
                if link:
                    article_url = link.get("href")
                    articles.append(
                        {"base_url": category["base_url"], "url": article_url}
                    )
    filename = save_articles(articles)
    Logging.echo(
        f"Collecting for {url} done! Total amount {len(articles)} in {len(categories)} categories."
    )
    Logging.echo(f'Saved to "{filename}"')


def scrape_svt(url) -> List:
    driver = init_Chrome()
    driver.get(url)
    cookie_ok_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, '// *[ @ id = "root"] / div[2] / div / div[3] / button[3]')
        )
    )
    cookie_ok_button.click()

    menu_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="nyh_a11y-primary-navigation-list"]/li[1]/a[2]')
        )
    )

    menu_item.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#nyh_a11y-primary-navigation-list > li:nth-child(1) > ul",
            )
        )
    )

    menu_html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(menu_html, "html.parser")
    Logging.echo(f"Start collecting urls for {url}")
    categories = []
    for category in soup.select(".MenuCard__link___QTXVS"):
        if category.get("href").startswith("/nyheter/"):
            category_url = category.get("href")
            category_name = category.text.strip()
            categories.append(
                {"base_url": url + category_url, "category_name": category_name}
            )

    articles = []
    for category in categories:
        response = requests.get(category["base_url"])
        soup = BeautifulSoup(response.content, "html.parser")
        for article in soup.find_all("a", class_="nyh_teaser__link"):
            article_url = article.get("href")
            articles.append(
                {"base_url": category["base_url"], "url": url + article_url}
            )
    filename = save_articles(articles)
    Logging.echo(
        f"Collecting for {url} done! Total amount {len(articles)} in {len(categories)} categories."
    )
    Logging.echo(f'Saved to "{filename}"')


def scrape_rtp(url) -> List:
    driver = init_Chrome()
    driver.get(url)

    cookie_ok_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
    )
    cookie_ok_button.click()

    menu_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "navbar-toggler"))
    )
    menu_item.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#nav-padder > ul:nth-child(2)")
        )
    )
    menu_html = driver.page_source
    soup = BeautifulSoup(menu_html, "html.parser")
    Logging.echo(f"Start collecting urls for {url}")
    categories = []
    menu_categories = soup.select("#nav-padder > ul:nth-child(2)")
    ul_element = menu_categories[0]
    for link in ul_element.find_all("a"):
        category_url = link.get("href")
        category_name = link.text.strip()
        if category_name == "Vídeos":
            break
        categories.append({"category_name": category_name, "base_url": category_url})

    articles = []
    for category in categories:
        driver.get(category["base_url"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#noticias > div.container.main-content.margin-top > div.row > div.sidebar_articles.col-12.col-lg-4.relative.bg-color.d-print-none.d-none.d-sm-none.d-lg-block > section",
                )
            )
        )
        news_bar = driver.page_source
        soup = BeautifulSoup(news_bar, "html.parser")
        for article in soup.find_all("article"):
            article_url = article.get("data-playlist-item-url")
            if article_url:
                articles.append({"base_url": category["base_url"], "url": article_url})
    driver.quit()
    filename = save_articles(articles)
    Logging.echo(
        f"Collecting for {url} done! Total amount {len(articles)} in {len(categories)} categories."
    )
    Logging.echo(f'Saved to "{filename}"')


def scrape_rtbf(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    Logging.echo(f"Start collecting urls for {url}")
    categories = []
    for cat in soup.find(
            "ul",
            "relative flex w-full select-none snap-x list-none flex-nowrap gap-6 overflow-x-auto lg:overflow-x-hidden sb-scroll-40 w-full gap-x-16",
    ).find_all("a", class_="outline-0"):
        category_url = cat.get("href").split("/")[-1]
        if category_url != "en-continu":
            category_name = cat.find("span", class_="pointer-events-none").get_text(
                strip=True
            )
            categories.append(
                {"category_name": category_name, "base_url": url + category_url}
            )

    articles = []
    for category in categories:
        for article in soup.find_all(
                "a", class_="stretched-link leading-[1.6rem] outline-none"
        ):
            article_url = article.get("href")
            articles.append(
                {
                    "base_url": category["base_url"],
                    "url": "https://www.rtbf.be" + article_url,
                }
            )
    filename = save_articles(articles)
    Logging.echo(
        f"Collecting for {url} done! Total amount {len(articles)} in {len(categories)} categories."
    )
    Logging.echo(f'Saved to "{filename}"')


def main() -> None:
    Logging.echo(f"Starting scraping... Keep calm :)")
    scrape_inews(CONFIG.INEWS_BASE)
    scrape_svt(CONFIG.SVT_BASE)
    scrape_rtp(CONFIG.RTP_BASE)
    scrape_rtbf(CONFIG.RTBF_BASE)
    Logging.echo("Successfully scraped!")


if __name__ == "__main__":
    main()
