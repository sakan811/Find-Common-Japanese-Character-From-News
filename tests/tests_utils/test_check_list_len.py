from jp_news_scraper_pipeline.jp_news_scraper.utils import check_list_len


def test_returns_tuple_of_lengths_for_multiple_lists_with_same_length():
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    list3 = [True, False, True]
    result = check_list_len(list1, list2, list3)
    assert result == (3, 3, 3)


def test_handles_no_input_lists_gracefully():
    result = check_list_len()
    assert result == ()


def test_handles_lists_with_none_values():
    # Setup
    target_list_1 = [1, 2, 3, None]
    target_list_2 = [4, None, 6, 7]
    target_list_3 = [None, 9, 10, 11]

    # Exercise
    result = check_list_len(target_list_1, target_list_2, target_list_3)

    # Verify
    assert result == (4, 4, 4)


def test_returns_tuple_of_lengths_for_multiple_lists_with_different_lengths():
    # Setup
    target_list_1 = ['apple', 'banana', 'cherry']
    target_list_2 = ['dog', 'cat']
    target_list_3 = ['red', 'blue', 'green', 'yellow']

    # Exercise
    result = check_list_len(target_list_1, target_list_2, target_list_3)

    # Verify
    assert result == (3, 2, 4)