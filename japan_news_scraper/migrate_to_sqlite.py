import logging
import sqlite3

from japan_news_scraper.data_transformer import fetch_exist_url_from_db, filter_out_urls_existed_in_db
from japanese_news_scraper import create_japan_news_table, create_news_url_table, process_new_hrefs


def migrate_to_sqlite(filtered_df, sqlite_db) -> None:
    """
    Save filtered DataFrame to SQLite database.
    :param filtered_df: Filtered DataFrame.
    :param sqlite_db: Sqlite database file path.
    :return: None
    """
    logging.info('Migrate data to SQLite database.')
    with sqlite3.connect(sqlite_db) as conn:
        create_japan_news_table(conn)
        filtered_df.to_sql('JapanNews', conn, if_exists='append', index=False)
        logging.info('Append to JapanNews table successfully.')


def get_new_urls(cleaned_href_list, sqlite_db) -> list[str]:
    """
    Get new urls from cleaned href list.
    :param cleaned_href_list: Cleaned href list.
    :param sqlite_db: SQLite database.
    :return: New urls as a list.
    """
    logging.info('Get new urls from cleaned href list.')
    with sqlite3.connect(sqlite_db) as conn:
        create_news_url_table(conn)
        existing_urls: list[str] = fetch_exist_url_from_db(conn)
        new_hrefs: list[str] = filter_out_urls_existed_in_db(existing_urls, cleaned_href_list)
        process_new_hrefs(conn, new_hrefs)
    return new_hrefs
