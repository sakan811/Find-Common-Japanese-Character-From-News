from morpheme_to_word import clean_jp_text_list


def test_normal_japanese_text():
    input_text = ["こんにちは", "世界"]
    expected_output = ["こんにちは", "世界"]
    assert clean_jp_text_list(input_text) == expected_output


def test_text_with_digits():
    input_text = ["こんにちは123", "世2界"]
    expected_output = ["こんにちは", "世界"]
    assert clean_jp_text_list(input_text) == expected_output


def test_text_with_punctuation():
    input_text = ["こんにちは!", "世界。"]
    expected_output = ["こんにちは", "世界"]
    assert clean_jp_text_list(input_text) == expected_output


def test_text_with_brackets():
    input_text = ["こ(ん)に(ち)は", "世[界]"]
    expected_output = ["こんにちは", "世界"]
    assert clean_jp_text_list(input_text) == expected_output


def test_mixed_text():
    input_text = ["helloこんにちは", "world世界"]
    expected_output = ["こんにちは", "世界"]
    assert clean_jp_text_list(input_text) == expected_output


def test_empty_string():
    input_text = [""]
    expected_output = []
    assert clean_jp_text_list(input_text) == expected_output


def test_only_non_japanese_text():
    input_text = ["hello", "123", "!@#"]
    expected_output = []
    assert clean_jp_text_list(input_text) == expected_output


def test_mixed_japanese_scripts():
    input_text = ["カタカナと漢字とひらがな", "テスト123"]
    expected_output = ["カタカナと漢字とひらがな", "テスト"]
    assert clean_jp_text_list(input_text) == expected_output
