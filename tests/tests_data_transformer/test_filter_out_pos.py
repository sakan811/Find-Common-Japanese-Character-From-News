import pytest
import pandas as pd

from jp_news_scraper_pipeline.jp_news_scraper.data_transformer import filter_out_pos


def test_filter_out_pos_empty():
    """
    Test filter_out_pos with an empty DataFrame.
    """
    df = pd.DataFrame(columns=['Kanji', 'PartOfSpeech'])
    expected_output = pd.DataFrame(columns=['Kanji', 'PartOfSpeech'])
    pd.testing.assert_frame_equal(filter_out_pos(df), expected_output)


def test_filter_out_pos_no_exclusion():
    """
    Test filter_out_pos with a DataFrame where no rows should be filtered.
    """
    df = pd.DataFrame({'Kanji': ['日本', 'こんにちは', '東京'], 'PartOfSpeech': ['名詞', '名詞', '名詞']})
    expected_output = df.copy()
    pd.testing.assert_frame_equal(filter_out_pos(df), expected_output)


def test_filter_out_pos_some_exclusion():
    """
    Test filter_out_pos with a DataFrame where some rows should be filtered.
    """
    df = pd.DataFrame({'Kanji': ['日本', '@@', 'こんにちは', ' ', '東京'],
                       'PartOfSpeech': ['名詞', '記号', '名詞', '空白', '名詞']})
    expected_output = pd.DataFrame({'Kanji': ['日本', 'こんにちは', '東京'], 'PartOfSpeech': ['名詞', '名詞', '名詞']},
                                   index=[0, 2, 4])
    pd.testing.assert_frame_equal(filter_out_pos(df), expected_output)


def test_filter_out_pos_all_exclusion():
    """
    Test filter_out_pos with a DataFrame where all rows should be filtered.
    """
    df = pd.DataFrame({'Kanji': ['@@@', ' '], 'PartOfSpeech': ['記号', '空白']})
    expected_output = pd.DataFrame(columns=['Kanji', 'PartOfSpeech'])
    pd.testing.assert_frame_equal(filter_out_pos(df), expected_output)


def test_filter_out_pos_special_characters():
    """
    Test filter_out_pos with a DataFrame containing special characters or non-Japanese parts of speech.
    """
    df = pd.DataFrame(
        {'Kanji': ['日本', 'こんにちは', '@#$', '東京'], 'PartOfSpeech': ['名詞', '名詞', '記号', '名詞']})
    expected_output = pd.DataFrame(
        {'Kanji': ['日本', 'こんにちは', '東京'], 'PartOfSpeech': ['名詞', '名詞', '名詞']}, index=[0, 1, 3])
    pd.testing.assert_frame_equal(filter_out_pos(df), expected_output)


if __name__ == "__main__":
    pytest.main()
