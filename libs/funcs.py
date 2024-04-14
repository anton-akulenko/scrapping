from __future__ import annotations

import inspect
import json
import os
from datetime import datetime
from typing import Any

from selenium import webdriver


def get_calling_function_name():
    # Get the call stack
    stack = inspect.stack()
    # The calling function is the one at index 2
    calling_function_name = stack[2].function
    return calling_function_name


def save_articles(articles: list[dict[str, Any]]) -> None:
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    calling_function_name = get_calling_function_name()
    directory_path = os.path.join(os.getcwd(), "data")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    filename = f"{calling_function_name}_{current_datetime}.json"
    file_path = os.path.join(directory_path, filename)
    with open(file_path, "w") as file:
        json.dump(articles, file, indent=4)
    return filename


def save(url, title, content, author, datetime_f, readable_f):
    data = [
        {
            "URL_article": url,
            "title": title,
            "content": content,
            "author": author,
            "date": datetime_f,
            "date_readable": readable_f,
        }
    ]
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    calling_function_name = get_calling_function_name()
    directory_path = os.path.join(os.getcwd(), "data")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    filename = f"{calling_function_name}_{current_datetime}.json"
    file_path = os.path.join(directory_path, filename)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    return filename


def convert_publication_date(date: str) -> tuple[str, Any]:
    date_time = datetime.fromisoformat(date.replace("Z", "+00:00"))
    full_date_time_format = date_time.strftime("%A, %d %B %Y, %H:%M:%S")
    return date_time.strftime("%Y-%m-%d_%H-%M-%S"), full_date_time_format


def init_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--ignore-gpu-blacklist")
    options.add_argument("--use-gl")
    options.add_argument("--disable-cookies")
    options.add_argument("--disable-web-security")
    driver = webdriver.Chrome(options=options)
    return driver
