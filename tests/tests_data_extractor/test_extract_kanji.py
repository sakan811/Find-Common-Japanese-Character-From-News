import pytest

from jp_news_scraper_pipeline.jp_news_scraper.data_extractor import extract_morphemes

# Sample test data
joined_text_list_with_kanji = ["これはテストです。", "漢字を抽出します。"]
joined_text_list_without_kanji = ["This is a test.", "No kanji here."]
empty_text_list = []


def test_extract_kanji_with_kanji():
    result = extract_morphemes(joined_text_list_with_kanji)
    assert result == ['これ', 'は', 'テスト', 'です', '。', '漢字', 'を', '抽出', 'する', 'ます', '。']


def test_extract_kanji_without_kanji():
    result = extract_morphemes(joined_text_list_without_kanji)
    assert result == ['This', ' ', 'is', ' ', 'a', ' ', 'test', '.', 'NO', ' ', 'kanji', ' ', 'Here', '.']


def test_extract_kanji_empty_list():
    result = extract_morphemes(empty_text_list)
    assert result == []


# Run the tests
if __name__ == "__main__":
    pytest.main()
