from jp_news_scraper_pipeline.jp_news_scraper.utils import check_if_all_list_len_is_equal


def test_all_lists_have_same_length():
    # Given
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    list3 = [True, False, True]

    # When
    result = check_if_all_list_len_is_equal(list1, list2, list3)

    # Then
    assert result is True


def test_one_list_is_empty_while_others_are_not():
    # Given
    list1 = []
    list2 = ['a', 'b', 'c']
    list3 = [True, False, True]

    # When
    result = check_if_all_list_len_is_equal(list1, list2, list3)

    # Then
    assert result is False


def test_empty_lists_equal_length():
    # Setup
    kanji_list = []
    pos_list = []
    pos_translated_list = []

    # Call
    result = check_if_all_list_len_is_equal(kanji_list, pos_list, pos_translated_list)

    # Assert
    assert result == True


def test_lists_of_different_lengths():
    # Create lists of different lengths
    kanji_list = ['日', '本', '語']
    pos_list = ['noun', 'noun']
    pos_translated_list = ['noun', 'noun', 'noun', 'noun']

    # Call the function and assert the result
    assert not check_if_all_list_len_is_equal(kanji_list, pos_list, pos_translated_list)