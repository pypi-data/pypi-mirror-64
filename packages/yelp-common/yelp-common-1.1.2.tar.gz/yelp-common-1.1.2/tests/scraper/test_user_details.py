from tests.scraper.resources import get_test_resource_soup
from yelp_fetcher.scraper.user_details import (
    get_user_city,
    get_user_details_url,
    get_user_name,
    get_user_review_count,
)


def test_get_user_details_url():
    # Given
    expected_urls = {
        "user_id_0": "https://www.yelp.com/user_details?userid=user_id_0",
        "user_id_1": "https://www.yelp.com/user_details?userid=user_id_1",
        "user_id_2": "https://www.yelp.com/user_details?userid=user_id_2",
    }

    for user_id, expected_url in expected_urls.items():
        # When
        url = get_user_details_url(user_id)

        # Then
        assert url == expected_url


def test_get_user_name():
    # Given
    test_cases = {
        get_test_resource_soup(
            "user_details/userid=5prk8CtPPBHNpa6BOja2ug.html"
        ): "Sam K.",
        get_test_resource_soup(
            "user_details/userid=uti2qXa5mupl2YqtrxHaOg.html"
        ): "G K.",
        get_test_resource_soup(
            "user_details/userid=Gx9m-uVNSAua8KdVyiQfGA.html"
        ): "Christina L.",
    }

    for user_page, expected in test_cases.items():
        # When
        result = get_user_name(user_page)

    # Then
    assert result == expected


def test_get_user_city():
    # Given
    test_cases = {
        get_test_resource_soup(
            "user_details/userid=5prk8CtPPBHNpa6BOja2ug.html"
        ): "Irvine, CA",
        get_test_resource_soup(
            "user_details/userid=uti2qXa5mupl2YqtrxHaOg.html"
        ): "Arcadia, CA",
        get_test_resource_soup(
            "user_details/userid=Gx9m-uVNSAua8KdVyiQfGA.html"
        ): "San Francisco, CA",
    }

    for user_page, expected in test_cases.items():
        # When
        result = get_user_city(user_page)

    # Then
    assert result == expected


def test_get_user_review_count():
    # Given
    test_cases = {
        get_test_resource_soup("user_details/userid=5prk8CtPPBHNpa6BOja2ug.html"): "17",
        get_test_resource_soup("user_details/userid=uti2qXa5mupl2YqtrxHaOg.html"): "14",
        get_test_resource_soup(
            "user_details/userid=Gx9m-uVNSAua8KdVyiQfGA.html"
        ): "223",
    }

    for user_page, expected in test_cases.items():
        # When
        result = get_user_review_count(user_page)

    # Then
    assert result == expected
