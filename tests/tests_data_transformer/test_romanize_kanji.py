import pytest
import cutlet


def romanize_kanji(kanji: str) -> str:
    """
    Romanize kanji.
    :param kanji: Kanji.
    :return: Romanized kanji.
    """
    return cutlet.Cutlet().romaji(kanji)


def test_romanize_kanji_empty():
    """
    Test romanize_kanji with an empty string.
    """
    assert romanize_kanji("") == ""


def test_romanize_kanji_single_kanji():
    """
    Test romanize_kanji with a single Kanji character.
    """
    kanji = "日"  # Replace with an actual Kanji character
    expected_output = "Hi"  # Replace with the expected Romanized output
    assert romanize_kanji(kanji) == expected_output


def test_romanize_kanji_multiple_kanji():
    """
    Test romanize_kanji with multiple Kanji characters.
    """
    kanji = "日本"  # Replace with actual Kanji characters
    expected_output = "Nippon"  # Replace with the expected Romanized output
    assert romanize_kanji(kanji) == expected_output


def test_romanize_kanji_mixed():
    """
    Test romanize_kanji with mixed Kanji and non-Kanji characters.
    """
    kanji = "今日は"  # Replace with a mix of Kanji and non-Kanji characters
    expected_output = "Kyou wa"  # Replace with the expected Romanized output
    assert romanize_kanji(kanji) == expected_output


def test_romanize_kanji_non_kanji():
    """
    Test romanize_kanji with non-Kanji characters.
    """
    kanji = "hello"  # Non-Kanji characters
    expected_output = "Hello"  # Expected output should be the same
    assert romanize_kanji(kanji) == expected_output


if __name__ == "__main__":
    pytest.main()
