from tests.scraper.resources import get_test_resource_soup
from yelp_fetcher.scraper.user_details_reviews_self import (
    ScrapedReview,
    get_user_biz_reviews,
    get_user_details_reviews_self_url,
)


def test_get_user_details_reviews_self_url():
    # Given
    user_id = "user_id"
    expected_urls = {
        0: "https://www.yelp.com/user_details_reviews_self?rec_pagestart=0&userid=user_id",
        1: "https://www.yelp.com/user_details_reviews_self?rec_pagestart=10&userid=user_id",
        2: "https://www.yelp.com/user_details_reviews_self?rec_pagestart=20&userid=user_id",
    }

    for page, expected_url in expected_urls.items():
        # When
        url = get_user_details_reviews_self_url(user_id, page)

        # Then
        assert url == expected_url


def test_get_user_biz_reviews():
    # Given
    review_page_0 = get_test_resource_soup(
        "user_details_reviews_self/user_details_reviews_self?userid=5prk8CtPPBHNpa6BOja2ug.html"
    )

    # When
    result = get_user_biz_reviews(review_page_0)

    # Then
    expected = [
        ScrapedReview(
            "bunker21-artesia", "Bunker21", "kzJihaxgEIphSySgBNNOiA", "1/2/2020",
        ),
        ScrapedReview(
            "chick-fil-a-cerritos",
            "Chick-fil-A",
            "dy_dxor2rVhpNuSUrrBw0w",
            "12/30/2019",
        ),
        ScrapedReview(
            "chipotle-mexican-grill-cerritos-9",
            "Chipotle Mexican Grill",
            "ofWhnV6m26kMyCpUjT56XA",
            "1/4/2020",
        ),
        ScrapedReview(
            "han-yang-buena-park", "Han Yang", "A_mJavYl2b4_oitezbpR8w", "12/28/2019",
        ),
        ScrapedReview(
            "la-mirada-golf-course-la-mirada",
            "La Mirada Golf Course",
            "7lJZPiK5-rBkojTxYS6R2w",
            "1/1/2020",
        ),
        ScrapedReview(
            "myung-dong-kyoja-anaheim-5",
            "Myung Dong Kyoja",
            "X0_-zEk0_CKj24wEEoau9A",
            "1/1/2020",
        ),
        ScrapedReview(
            "panda-express-cerritos",
            "Panda Express",
            "-eb-SRIXvQ_tyJKFldJMyw",
            "12/29/2019",
        ),
        ScrapedReview(
            "roger-dunn-golf-shops-seal-beach-3",
            "Roger Dunn Golf Shops",
            "Ve3BLwnfMTXZMwCViW-MLg",
            "12/31/2019",
        ),
        ScrapedReview(
            "thai-addict-cuisine-buena-park-2",
            "Thai Addict Cuisine",
            "ZfHJEeZFKTPFwAJGMYiXrA",
            "12/31/2019",
        ),
        ScrapedReview("yoko-buena-park", "Yoko", "MS1f3LaFfHeh5kcF2qt-1A", "1/3/2020",),
    ]
    assert set(result) == set(expected)


def test_get_user_biz_reviews_none():
    # Given
    page_no_reviews = get_test_resource_soup(
        "user_details_reviews_self/user_details_reviews_self?userid=yOdiJSKdFuE6EsAfd7jDKQ.html"
    )

    # When
    result = get_user_biz_reviews(page_no_reviews)

    # Then
    expected = []
    assert set(result) == set(expected)
