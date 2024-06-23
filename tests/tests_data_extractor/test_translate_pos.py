import pytest

from jp_news_scraper_pipeline.jp_news_scraper.data_extractor import translate_pos


def test_translate_pos_empty_list():
    """
    Test translate_pos with an empty list.
    """
    assert translate_pos([]) == []


def test_translate_pos_single_pos():
    """
    Test translate_pos with a single part of speech.
    """
    part_of_speech_list = ["名詞"]
    expected_output = ["Noun"]
    assert translate_pos(part_of_speech_list) == expected_output


def test_translate_pos_multiple_pos():
    """
    Test translate_pos with multiple parts of speech.
    """
    part_of_speech_list = ["名詞", "動詞", "形容詞"]
    expected_output = ["Noun", "Verb", "Adjective"]
    assert translate_pos(part_of_speech_list) == expected_output


def test_translate_pos_invalid_pos():
    """
    Test translate_pos with an invalid part of speech.
    """
    part_of_speech_list = ["invalid_pos"]
    with pytest.raises(KeyError):
        translate_pos(part_of_speech_list)


if __name__ == "__main__":
    pytest.main()
