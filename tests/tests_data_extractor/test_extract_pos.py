import pytest

from jp_news_scraper_pipeline.jp_news_scraper.data_extractor import extract_pos


def test_extract_pos_empty_list():
    """
    Test extract_pos with an empty list.
    """
    assert extract_pos([]) == []


def test_extract_pos_single_kanji():
    """
    Test extract_pos with a single Kanji character.
    """
    kanji_list = ["日"]
    expected_output = ["名詞"]
    assert extract_pos(kanji_list) == expected_output


def test_extract_pos_multiple_kanji():
    """
    Test extract_pos with multiple Kanji characters.
    """
    kanji_list = ["日", "月", "火"]
    expected_output = ['名詞', '名詞', '名詞']
    assert extract_pos(kanji_list) == expected_output


def test_extract_pos_non_kanji():
    """
    Test extract_pos with non-Kanji characters.
    """
    kanji_list = ["a", "b", "c"]
    expected_output = ['名詞', '名詞', '名詞']
    assert extract_pos(kanji_list) == expected_output


if __name__ == "__main__":
    pytest.main()
