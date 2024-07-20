from jp_news_scraper_pipeline.pipeline import get_new_urls


def test_returns_new_urls(mocker):
    # Given
    cleaned_url_list = ['http://example.com/1', 'http://example.com/2']
    sqlite_db = ':memory:'
    existing_urls = ['http://example.com/1']
    expected_new_urls = ['http://example.com/2']

    # Mock dependencies
    mocker.patch('jp_news_scraper_pipeline.pipeline.fetch_exist_url_from_db', return_value=existing_urls)
    mocker.patch('jp_news_scraper_pipeline.pipeline.filter_out_urls_existed_in_db', return_value=expected_new_urls)

    # When
    new_urls = get_new_urls(cleaned_url_list, sqlite_db)

    # Then
    assert new_urls == expected_new_urls


def test_handles_empty_cleaned_url_list_gracefully(mocker):
    # Given an empty cleaned URL list
    cleaned_url_list = []
    sqlite_db = ':memory:'

    # Mock dependencies
    # Assume these functions are part of the same module as get_new_urls
    mocker.patch('jp_news_scraper_pipeline.pipeline.fetch_exist_url_from_db', return_value=[])
    mocker.patch('jp_news_scraper_pipeline.pipeline.filter_out_urls_existed_in_db', return_value=[])

    # When calling the get_new_urls function
    new_urls = get_new_urls(cleaned_url_list, sqlite_db)

    # Then ensure the new_urls list is also empty
    assert new_urls == []