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
