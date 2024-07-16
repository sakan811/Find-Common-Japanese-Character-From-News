from morpheme_to_word import combine_morpheme_to_word


def test_combine_morpheme_to_word_single_word():
    morphemes = ['こ', 'ん', 'に', 'ち', 'は']
    dictionary = {'こんにちは'}
    expected_output = ['こんにちは']
    assert combine_morpheme_to_word(morphemes, dictionary) == expected_output


def test_combine_morpheme_to_word_multiple_words():
    morphemes = ['さ', 'よ', 'う', 'な', 'ら']
    dictionary = {'さようなら', 'さよなら'}
    expected_output = ['さようなら']
    assert combine_morpheme_to_word(morphemes, dictionary) == expected_output


def test_combine_morpheme_to_word_partial_words():
    morphemes = ['た', 'べ', 'に', '行', 'っ', 'た']
    dictionary = {'たべに', '行った', 'った'}
    expected_output = ['たべに', '行った']
    assert combine_morpheme_to_word(morphemes, dictionary) == expected_output


def test_combine_morpheme_to_word_long_morphemes():
    morphemes = ['き', 'れ', 'い', 'な', 'ケ', 'ーキ', 'が', '好', 'き', 'だ']
    dictionary = {'きれい', 'ケーキ', '好き', 'だ'}
    expected_output = ['きれい', 'ケーキ', '好き', 'だ']
    assert combine_morpheme_to_word(morphemes, dictionary) == expected_output


def test_combine_morpheme_to_word_no_valid_words():
    morphemes = ['あ', 'い', 'う', 'え', 'お']
    dictionary = {'こんにちは', 'さようなら'}
    expected_output = []
    assert combine_morpheme_to_word(morphemes, dictionary) == expected_output
