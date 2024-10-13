import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, call
from main import start_news_scraper_pipeline


@pytest.fixture
def mock_sqlite3():
    with patch('main.sqlite3') as mock:
        yield mock


@pytest.fixture
def mock_logger():
    with patch('main.logger') as mock:
        yield mock


def test_successful_pipeline(mock_sqlite3, mock_logger, tmp_path):
    with patch('main.get_cleaned_url_list') as mock_get_cleaned_url_list, \
            patch('main.get_new_urls') as mock_get_new_urls, \
            patch('main.extract_data') as mock_extract_data, \
            patch('main.transform_data_to_df') as mock_transform_data_to_df:
        mock_get_cleaned_url_list.return_value = ['url1', 'url2']
        mock_get_new_urls.return_value = ['url1', 'url2']
        mock_extract_data.return_value = (['kanji1', 'kanji2'], ['pos1', 'pos2'], ['trans1', 'trans2'])
        mock_transform_data_to_df.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        db_path = str(tmp_path / 'test.db')
        result = start_news_scraper_pipeline(db_path)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        mock_logger.warning.assert_not_called()
        mock_logger.error.assert_not_called()


def test_no_new_urls(mock_sqlite3, mock_logger, tmp_path):
    with patch('main.get_cleaned_url_list') as mock_get_cleaned_url_list, \
            patch('main.get_new_urls') as mock_get_new_urls:
        mock_get_cleaned_url_list.return_value = ['url1', 'url2']
        mock_get_new_urls.return_value = []

        db_path = str(tmp_path / 'test.db')
        result = start_news_scraper_pipeline(db_path)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

        # Check that both warning messages were called in the correct order
        mock_logger.warning.assert_has_calls([
            call("No new URL found."),
            call("Return an empty DataFrame.")
        ])

        # Ensure that warning was called exactly twice
        assert mock_logger.warning.call_count == 2


def test_no_urls_found(mock_sqlite3, mock_logger):
    with patch('main.get_cleaned_url_list') as mock_get_cleaned_url_list:
        mock_get_cleaned_url_list.return_value = []

        result = start_news_scraper_pipeline('test.db')

        assert isinstance(result, pd.DataFrame)
        assert result.empty
        mock_logger.error.assert_called_with(
            "No URL found. Please check the tag in 'extract_href_tags' function in 'news_scraper.py'.")
        mock_logger.warning.assert_called_with("Return an empty DataFrame.")

        # Ensure that error was called once and warning was called once
        assert mock_logger.error.call_count == 1
        assert mock_logger.warning.call_count == 1


def test_database_operations(mock_sqlite3, mock_logger, tmp_path):
    mock_conn = MagicMock()
    mock_sqlite3.connect.return_value.__enter__.return_value = mock_conn

    with patch('main.get_cleaned_url_list') as mock_get_cleaned_url_list, \
            patch('main.get_new_urls') as mock_get_new_urls, \
            patch('main.extract_data') as mock_extract_data, \
            patch('main.transform_data_to_df') as mock_transform_data_to_df, \
            patch('main.create_news_url_table') as mock_create_news_url_table, \
            patch('main.load_new_urls_to_db') as mock_load_new_urls_to_db:
        mock_get_cleaned_url_list.return_value = ['url1', 'url2']
        mock_get_new_urls.return_value = ['url1', 'url2']
        mock_extract_data.return_value = (['kanji1', 'kanji2'], ['pos1', 'pos2'], ['trans1', 'trans2'])
        mock_transform_data_to_df.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        db_path = str(tmp_path / 'test.db')
        start_news_scraper_pipeline(db_path)

        mock_create_news_url_table.assert_called_once_with(mock_conn)
        mock_load_new_urls_to_db.assert_called_once_with(mock_conn, ['url1', 'url2'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
