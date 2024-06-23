import pytest

from jp_news_scraper_pipeline.jp_news_scraper.data_transformer import clean_url_list


def test_clean_url_list_empty():
    """
    Test clean_url_list with an empty list.
    """
    assert clean_url_list([]) == []


def test_clean_url_list():
    initial_urls = [
        "#section1",
        "https://example.com",
        "//www3.nhk.or.jp/senkyo2/shutoken/20336/skh54664.html",
        "http://example.com",
        "ftp://example.com"
    ]
    expected_output = [
        "/senkyo2/shutoken/20336/skh54664.html",
        "http://example.com",
        "ftp://example.com"
    ]
    assert clean_url_list(initial_urls) == expected_output


def test_clean_url_list_valid_urls():
    """
    Test clean_url_list with a list of valid URLs.
    """
    initial_urls = ["http://example.com", "ftp://example.com"]
    expected_output = ["http://example.com", "ftp://example.com"]
    assert clean_url_list(initial_urls) == expected_output


def test_clean_url_list_urls_with_hash():
    """
    Test clean_url_list with URLs starting with '#'.
    """
    initial_urls = ["#section1", "#section2"]
    expected_output = []
    assert clean_url_list(initial_urls) == expected_output


def test_clean_url_list_urls_with_https():
    """
    Test clean_url_list with URLs starting with 'https:'.
    """
    initial_urls = ["https://example.com", "https://example.org"]
    expected_output = []
    assert clean_url_list(initial_urls) == expected_output


def test_clean_url_list_mixed_urls():
    """
    Test clean_url_list with a mixed list of valid and unwanted URLs.
    """
    initial_urls = ["http://example.com", "#section1", "https://example.org", "ftp://example.com"]
    expected_output = ["http://example.com", "ftp://example.com"]
    assert clean_url_list(initial_urls) == expected_output


if __name__ == "__main__":
    pytest.main()
