from collections import namedtuple
from typing import List

from yelp_fetcher._util import fetch_soup
from yelp_fetcher.scraper.common import get_num_pages
from yelp_fetcher.scraper.user_details_reviews_self import (
    ScrapedReview,
    get_user_biz_reviews,
    get_user_details_reviews_self_url,
)


class Review(namedtuple("Review", "biz_id biz_name review_id review_date")):
    @staticmethod
    def from_scraped_review(scraped_review: ScrapedReview):
        return Review(
            biz_id=scraped_review.biz_id,
            biz_name=scraped_review.biz_name,
            review_id=scraped_review.review_id,
            review_date=scraped_review.review_date,
        )


def get_urls(user_id) -> List[str]:
    url = get_user_details_reviews_self_url(user_id)
    first_user_biz_soup = fetch_soup(url)
    num_user_biz_pages = get_num_pages(first_user_biz_soup)
    urls = map(
        lambda i: get_user_details_reviews_self_url(user_id, i),
        range(num_user_biz_pages),
    )
    return list(urls)


def get_reviews(url) -> List[Review]:
    user_biz_soup = fetch_soup(url)
    scraped_reviews = get_user_biz_reviews(user_biz_soup)
    reviews = map(lambda x: Review.from_scraped_review(x), scraped_reviews)
    return list(reviews)
