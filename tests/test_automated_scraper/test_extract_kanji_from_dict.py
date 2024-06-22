import pandas as pd
import pytest

from automated_news_scraper import extract_kanji_from_dict

# Sample test data
sample_dict_with_kanji = {
    "https://example.com/1": ["これはテストです。", "漢字を抽出します。"]
}
sample_dict_without_kanji = {
    "https://example.com/2": ["This is a test.", "No kanji here."]
}
empty_dict = {}


def test_extract_kanji_from_dict_with_kanji():
    expected_data = [
        ("https://example.com/1", "これ"),
        ("https://example.com/1", "は"),
        ("https://example.com/1", "テスト"),
        ("https://example.com/1", "です"),
        ("https://example.com/1", "。"),
        ("https://example.com/1", "漢字"),
        ("https://example.com/1", "を"),
        ("https://example.com/1", "抽出"),
        ("https://example.com/1", "する"),
        ("https://example.com/1", "ます"),
        ("https://example.com/1", "。")
    ]

    expected_df = pd.DataFrame(expected_data, columns=['Source', 'Kanji'])
    result_df = extract_kanji_from_dict(sample_dict_with_kanji)

    pd.testing.assert_frame_equal(result_df, expected_df)


def test_extract_kanji_from_dict_without_kanji():
    expected_data = [
        ("https://example.com/2", "This"),
        ("https://example.com/2", " "),
        ("https://example.com/2", "is"),
        ("https://example.com/2", " "),
        ("https://example.com/2", "a"),
        ("https://example.com/2", " "),
        ("https://example.com/2", "test"),
        ("https://example.com/2", "."),
        ("https://example.com/2", "NO"),
        ("https://example.com/2", " "),
        ("https://example.com/2", "kanji"),
        ("https://example.com/2", " "),
        ("https://example.com/2", "Here"),
        ("https://example.com/2", ".")
    ]

    expected_df = pd.DataFrame(expected_data, columns=['Source', 'Kanji'])
    result_df = extract_kanji_from_dict(sample_dict_without_kanji)

    pd.testing.assert_frame_equal(result_df, expected_df)


def test_extract_kanji_from_dict_empty_dict():
    result_df = extract_kanji_from_dict(empty_dict)

    assert result_df.empty


# Run the tests
if __name__ == "__main__":
    pytest.main()
