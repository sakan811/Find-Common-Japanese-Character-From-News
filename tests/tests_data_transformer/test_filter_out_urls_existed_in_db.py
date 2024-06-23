import pytest

from jp_news_scraper_pipeline.jp_news_scraper.data_transformer import filter_out_urls_existed_in_db


def test_filter_out_urls_existed_in_db_empty_lists():
    """
    Test filter_out_urls_existed_in_db with both lists empty.
    """
    assert filter_out_urls_existed_in_db([], []) == []


def test_filter_out_urls_existed_in_db_all_new_urls():
    """
    Test filter_out_urls_existed_in_db with all new URLs.
    """
    existing_urls = ["http://existing.com"]
    urls = ["http://new1.com", "http://new2.com"]
    expected_output = ["http://new1.com", "http://new2.com"]
    assert filter_out_urls_existed_in_db(existing_urls, urls) == expected_output


def test_filter_out_urls_existed_in_db_some_existing_urls():
    """
    Test filter_out_urls_existed_in_db with some existing URLs.
    """
    existing_urls = ["http://existing.com"]
    urls = ["http://new1.com", "http://existing.com"]
    expected_output = ["http://new1.com"]
    assert filter_out_urls_existed_in_db(existing_urls, urls) == expected_output


def test_filter_out_urls_existed_in_db_all_existing_urls():
    """
    Test filter_out_urls_existed_in_db with all URLs existing.
    """
    existing_urls = ["http://existing.com", "http://existing2.com"]
    urls = ["http://existing.com", "http://existing2.com"]
    expected_output = []
    assert filter_out_urls_existed_in_db(existing_urls, urls) == expected_output


if __name__ == "__main__":
    pytest.main()
