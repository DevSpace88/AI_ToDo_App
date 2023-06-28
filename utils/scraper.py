from pathlib import Path

from urllib.parse import urlparse

from bs4 import BeautifulSoup

import requests


def django_docs_build_urls():
    root_url = "https://docs.djangoproject.com/en/4.2/contents/"
    root_response = requests.get(root_url)
    root_html = root_response.content.decode("utf-8")
    soup = BeautifulSoup(root_html, 'html.parser')

    root_url_parts = urlparse(root_url)
    root_links = soup.find_all("a", attrs={"class": "reference internal"})

    result = set()

    for root_link in root_links:
        path = root_url_parts.path + root_link.get("href")
        path = str(Path(path).resolve())
        path = urlparse(path).path  # remove the hashtag

        url = f"{root_url_parts.scheme}://{root_url_parts.netloc}{path}"

        if not url.endswith("/"):
            url = url + "/"

        result.add(url)

    return list(result)