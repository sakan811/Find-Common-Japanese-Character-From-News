# This test is for testing the chunk calculation
# in 'process_list_of_text_lists_concurrently' function in 'morpheme_to_word.py'
import logging

import pytest

from morpheme_to_word import calculate_chunk_list


def test_chunk_list_even_chunks():
    text_list = ['a', 'b', 'c', 'd', 'e', 'f']
    num_chunk = 3
    expected_chunks = [['a', 'b'], ['c', 'd'], ['e', 'f']]
    assert calculate_chunk_list(text_list, num_chunk) == expected_chunks


def test_chunk_list_uneven_chunks():
    text_list = ['a', 'b', 'c', 'd', 'e']
    num_chunk = 2
    expected_chunks = [['a', 'b'], ['c', 'd'], ['e']]
    assert calculate_chunk_list(text_list, num_chunk) == expected_chunks


def test_chunk_list_single_chunk():
    text_list = ['a', 'b', 'c', 'd', 'e']
    num_chunk = 1
    expected_chunks = [['a', 'b', 'c', 'd', 'e']]
    assert calculate_chunk_list(text_list, num_chunk) == expected_chunks


def test_chunk_list_more_chunks_than_elements(caplog):
    text_list = ['a', 'b']
    num_chunk = 3
    expected_chunks = [['a', 'b']]

    with caplog.at_level(logging.WARNING):
        chunks = calculate_chunk_list(text_list, num_chunk)

    assert chunks == expected_chunks
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert caplog.records[0].message == 'Chunk size is 0. Adjust the chunk size to 2.'


def test_chunk_list_empty_list():
    text_list = []
    num_chunk = 3
    expected_chunks = []
    assert calculate_chunk_list(text_list, num_chunk) == expected_chunks


if __name__ == "__main__":
    pytest.main()
