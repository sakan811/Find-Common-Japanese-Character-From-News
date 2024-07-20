import pytest

from jp_news_scraper_pipeline.pipeline import extract_data


def test_extract_data_from_valid_urls(mocker):
    # Given
    new_urls = ['url1', 'url2']
    expected_morphemes = ['morpheme1', 'morpheme2']
    expected_pos = ['pos1', 'pos2']
    expected_translated_pos = ['translated_pos1', 'translated_pos2']

    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_text_from_url_list', return_value=['text1', 'text2'])
    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_morphemes', return_value=expected_morphemes)
    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_pos', return_value=expected_pos)
    mocker.patch('jp_news_scraper_pipeline.pipeline.translate_pos', return_value=expected_translated_pos)
    mocker.patch('jp_news_scraper_pipeline.pipeline.check_if_all_list_len_is_equal', return_value=True)

    # When
    result = extract_data(new_urls)

    # Then
    assert result == (expected_morphemes, expected_pos, expected_translated_pos)


def test_handle_empty_url_list(mocker):
    # Given
    new_urls = []

    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_text_from_url_list', return_value=[])
    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_morphemes', return_value=[])
    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_pos', return_value=[])
    mocker.patch('jp_news_scraper_pipeline.pipeline.translate_pos', return_value=[])
    mocker.patch('jp_news_scraper_pipeline.pipeline.check_if_all_list_len_is_equal', return_value=True)

    # When
    result = extract_data(new_urls)

    # Then
    assert result == ([], [], [])


def test_raise_value_error_when_list_lengths_not_equal(mocker):
    # Given
    new_urls = ['url1', 'url2', 'url3']
    morpheme_list = ['morpheme1', 'morpheme2']
    pos_list = ['pos1', 'pos2', 'pos3']
    pos_translated_list = ['translated_pos1', 'translated_pos2']

    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_text_from_url_list', return_value=['text1', 'text2', 'text3'])
    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_morphemes', return_value=morpheme_list)
    mocker.patch('jp_news_scraper_pipeline.pipeline.extract_pos', return_value=pos_list)
    mocker.patch('jp_news_scraper_pipeline.pipeline.translate_pos', return_value=pos_translated_list)
    mocker.patch('jp_news_scraper_pipeline.pipeline.check_if_all_list_len_is_equal', return_value=False)

    # When, Then
    with pytest.raises(ValueError) as e:
        extract_data(new_urls)

    assert str(e.value) == "The length of kanji_list, pos_list, and pos_translated_list are not equal."