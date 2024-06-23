import pandas as pd
import pytest

from jp_news_scraper_pipeline.jp_news_scraper.data_transformer import filter_out_non_jp_characters


def test_filter_out_non_jp_characters_empty():
    """
    Test filter_out_non_jp_characters with an empty DataFrame.
    """
    df = pd.DataFrame(columns=['Kanji'])
    expected_output = pd.DataFrame(columns=['Kanji'])
    pd.testing.assert_frame_equal(filter_out_non_jp_characters(df), expected_output)


def test_filter_out_non_jp_characters_only_japanese():
    """
    Test filter_out_non_jp_characters with a DataFrame containing only Japanese characters.
    """
    df = pd.DataFrame({'Kanji': ['日本', 'こんにちは', '東京']})
    expected_output = pd.DataFrame({'Kanji': ['日本', 'こんにちは', '東京']})
    pd.testing.assert_frame_equal(filter_out_non_jp_characters(df), expected_output)


def test_filter_out_non_jp_characters_mixed():
    """
    Test filter_out_non_jp_characters with a DataFrame containing mixed characters.
    """
    df = pd.DataFrame({'Kanji': ['日本', 'hello', 'こんにちは', '123', '東京']})
    expected_output = pd.DataFrame({'Kanji': ['日本', 'こんにちは', '東京']}, index=[0, 2, 4])
    pd.testing.assert_frame_equal(filter_out_non_jp_characters(df), expected_output)


def test_filter_out_non_jp_characters_only_non_japanese():
    """
    Test filter_out_non_jp_characters with a DataFrame containing only non-Japanese characters.
    """
    df = pd.DataFrame({'Kanji': ['hello', 'world', '123', 'abc']})
    expected_output = pd.DataFrame(columns=['Kanji'])
    pd.testing.assert_frame_equal(filter_out_non_jp_characters(df), expected_output)


def test_filter_out_non_jp_characters_special_characters():
    """
    Test filter_out_non_jp_characters with a DataFrame containing special characters.
    """
    df = pd.DataFrame({'Kanji': ['日本', 'こんにちは', '@#$', '東京']})
    expected_output = pd.DataFrame({'Kanji': ['日本', 'こんにちは', '@#$', '東京']})
    pd.testing.assert_frame_equal(filter_out_non_jp_characters(df), expected_output)


if __name__ == "__main__":
    pytest.main()
