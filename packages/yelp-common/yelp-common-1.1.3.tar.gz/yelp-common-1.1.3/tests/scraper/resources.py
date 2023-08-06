import os

from bs4 import BeautifulSoup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def get_test_resource_path(path):
    """Get file given a path, relative to scraper/tests/html"""
    result = os.path.join(THIS_DIR, "html", path)
    return result


def get_test_resource_html(path):
    """Get HTML given a path, relative to scraper/tests/html"""
    with open(get_test_resource_path(path)) as f:
        return f.read()


def get_test_resource_soup(path):
    """Get BS4 BeautifulSoup given a path, relative to scraper/tests/html"""
    with open(get_test_resource_path(path)) as f:
        return BeautifulSoup(f.read(), "html.parser")
