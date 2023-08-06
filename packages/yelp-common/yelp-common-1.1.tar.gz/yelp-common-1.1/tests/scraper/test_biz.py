from tests.scraper.resources import get_test_resource_path
from yelp_fetcher.scraper.biz import get_biz_review_url, review_id_on_page


def test_get_biz_review_url():
    # Given
    expected_urls = {
        ("biz0", "rev0"): "https://www.yelp.com/biz/biz0?hrid=rev0",
        ("biz1", "rev1"): "https://www.yelp.com/biz/biz1?hrid=rev1",
        ("biz2", "rev2"): "https://www.yelp.com/biz/biz2?hrid=rev2",
    }

    for (biz_id, review_id), expected_url in expected_urls.items():
        # When
        url = get_biz_review_url(biz_id, review_id)

        # Then
        assert url == expected_url


def test_review_id_on_page_yes():
    # Given
    filenames = {
        "ct_w8SKNRmrwxqmXTRe_rw": "biz/chipotle-mexican-grill-cerritos-9?hrid=ct_w8SKNRmrwxqmXTRe_rw.html",
        "HcLsMKuQT3KHgf6-0J0zMw": "biz/aloha-family-billiards-buena-park?hrid=HcLsMKuQT3KHgf6-0J0zMw.html",
        "VcmUwOpWndm0AKvvmwW9NA": "biz/bunker21-artesia?hrid=VcmUwOpWndm0AKvvmwW9NA.html",
    }

    # When
    for review_id, path in filenames.items():
        with open(get_test_resource_path(path)) as f:
            result = review_id_on_page(f.read(), review_id)

            # Then
            assert result


def test_review_id_on_page_no():
    # Given
    filenames = {
        "ofWhnV6m26kMyCpUjT56XA": "biz/chipotle-mexican-grill-cerritos-9?hrid=ofWhnV6m26kMyCpUjT56XA.html",
        "XMjUx1JAw4GVEhGGY4MoYw": "biz/aloha-family-billiards-buena-park?hrid=XMjUx1JAw4GVEhGGY4MoYw.html",
        "4Kw3pCYa_cm3g_lyqppC9g": "biz/bunker21-artesia?hrid=4Kw3pCYa_cm3g_lyqppC9g.html",
    }

    # When
    for review_id, path in filenames.items():
        with open(get_test_resource_path(path)) as f:
            result = review_id_on_page(f.read(), review_id)

            # Then
            assert not result
