from tests.scraper.resources import get_test_resource_soup
from yelp_fetcher.scraper.common import get_num_pages, get_review_ids


def test_get_review_ids_user_review_page():
    # Given
    soup_reviews_page = get_test_resource_soup(
        "user_details_reviews_self/user_details_reviews_self?userid=5prk8CtPPBHNpa6BOja2ug.html"
    )

    # When
    result = get_review_ids(soup_reviews_page)

    # Then
    expected = [
        "ofWhnV6m26kMyCpUjT56XA",
        "MS1f3LaFfHeh5kcF2qt-1A",
        "kzJihaxgEIphSySgBNNOiA",
        "7lJZPiK5-rBkojTxYS6R2w",
        "X0_-zEk0_CKj24wEEoau9A",
        "Ve3BLwnfMTXZMwCViW-MLg",
        "ZfHJEeZFKTPFwAJGMYiXrA",
        "dy_dxor2rVhpNuSUrrBw0w",
        "-eb-SRIXvQ_tyJKFldJMyw",
        "A_mJavYl2b4_oitezbpR8w",
    ]
    assert set(result) == set(expected)


def test_get_review_ids_not_recommended_page():
    # Given
    soup_not_recc = get_test_resource_soup(
        "not_recommended_reviews/not_recommended_reviews_súp-noodle-bar-buena-park-buena-park.html"
    )

    # When
    result = get_review_ids(soup_not_recc)

    # Then
    expected = [
        "04-z0KafkNno3SJROYOZXg",
        "6_Q_M3P9m-2RCKdJzvAWpw",
        "7mDLwDZDRB_8NOxv32F1ZQ",
        "94e2ewMKPQVZ1PmnS4uUSQ",
        "CTpZ1v4rGDM55jJ3S3yxZg",
        "ISo45SEdiOdLWZDVXBcMwQ",
        "J62o0SpdCIsANZx8seufEg",
        "O6aj9IDB4kwn7CY-L7cfAQ",
        "W17B30zLlM9zcy0LhH8AfA",
        "X8guNsPPamxl8568pwuHdw",
        "Xml9y-R6zuc1vL3jZXGAzA",
        "ZNz_v0117JiXIS4xu1xfRw",
        "eKE5nnpUmJ79QQ5OHiCTqA",
        "hRIocQbe87YebNkBgZfqCQ",
        "mHrxc6L0-E1Hu32hN-TSEg",
        "mfTknfdIohktWouPgqS2wQ",
        "nbSZnnEoUSv7IrwRdDnFMw",
        "rAjxjUm-x5SQ3XDii1-4AA",
        "rh7E1MRtAJ8Ql4JtAjwhEA",
        "riucV6WDfaDBzH5DUH3hOQ",
    ]
    assert set(result) == set(expected)


def test_get_review_ids_not_recommended_page_none():
    # Given
    soup_not_recc = get_test_resource_soup(
        "not_recommended_reviews/not_recommended_reviews_pho-ngon-norwalk-norwalk-2.html"
    )

    # When
    result = get_review_ids(soup_not_recc)

    # Then
    assert result == []


def test_get_num_pages_user_review_page():
    # Given
    soup_reviews_page = get_test_resource_soup(
        "user_details_reviews_self/user_details_reviews_self?userid=5prk8CtPPBHNpa6BOja2ug.html"
    )

    # When
    result = get_num_pages(soup_reviews_page)

    # Then
    assert result == 2


def test_get_num_pages_not_recommended_page():
    # Given
    soup_not_recc = get_test_resource_soup(
        "not_recommended_reviews/not_recommended_reviews_súp-noodle-bar-buena-park-buena-park.html"
    )

    # When
    result = get_num_pages(soup_not_recc)

    # Then
    assert result == 13


def test_get_num_pages_none():
    # Given
    soup_not_recc = get_test_resource_soup(
        "user_details_reviews_self/user_details_reviews_self?userid=yOdiJSKdFuE6EsAfd7jDKQ.html"
    )

    # When
    result = get_num_pages(soup_not_recc)

    # Then
    assert result == 0
