from tests.scraper.resources import get_test_resource_path
from yelp_fetcher.scraper.bs4_util import (
    get_element_by_classname,
    get_elements_by_classname,
    to_soup,
)


def test_to_soup():
    # Given
    with open(get_test_resource_path("bs4_util/sam_kim_yelp.html")) as f:
        text = f.read()

    # When
    soup = to_soup(text)

    # Then
    assert soup
    assert soup.title.string == "Sam K.'s Reviews | Irvine - Yelp"


def test_get_elements_by_classname_none():
    # Given
    with open(get_test_resource_path("bs4_util/sam_kim_yelp.html")) as f:
        text = f.read()
        soup = to_soup(text)

    # When
    elements = get_elements_by_classname(soup, "this-class-doesnt-exist")

    # Then
    assert len(elements) == 0


def test_get_elements_by_classname_exists():
    # Given
    with open(get_test_resource_path("bs4_util/sam_kim_yelp.html")) as f:
        text = f.read()
        soup = to_soup(text)

    # When
    elements = get_elements_by_classname(soup, "titled-nav_item")

    # Then
    assert len(elements) == 5


def test_get_element_by_classname_none():
    # Given
    with open(get_test_resource_path("bs4_util/sam_kim_yelp.html")) as f:
        text = f.read()
        soup = to_soup(text)

    # When
    result = get_element_by_classname(soup, "this-class-doesnt-exist")

    # Then
    assert result is None


def test_get_element_by_classname_exists():
    # Given
    with open(get_test_resource_path("bs4_util/sam_kim_yelp.html")) as f:
        text = f.read()
        soup = to_soup(text)

    # When
    element = get_element_by_classname(soup, "user-profile_info")

    # Then
    assert element
