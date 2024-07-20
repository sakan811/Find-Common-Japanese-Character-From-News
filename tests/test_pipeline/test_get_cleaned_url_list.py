from jp_news_scraper_pipeline.pipeline import get_cleaned_url_list


def test_returns_cleaned_url_list_for_valid_initial_url():
    # Given
    initial_url = 'https://www3.nhk.or.jp/news/'

    # When
    cleaned_url_list = get_cleaned_url_list(initial_url)

    # Then
    assert isinstance(cleaned_url_list, list)
    assert all(isinstance(url, str) for url in cleaned_url_list)


def test_handles_network_errors():
    # Given
    initial_url = "https://example.com"

    # When
    cleaned_url_list = get_cleaned_url_list(initial_url)

    # Then
    assert cleaned_url_list == []
