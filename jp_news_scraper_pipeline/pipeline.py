import logging
import sqlite3

import pandas as pd

from jp_news_scraper_pipeline.jp_news_scraper.data_extractor import extract_kanji, extract_pos, translate_pos
from jp_news_scraper_pipeline.jp_news_scraper.data_transformer import create_df_for_japan_news_table, \
    filter_out_non_jp_characters, \
    filter_out_pos, clean_url_list, filter_out_urls_existed_in_db, process_new_urls
from jp_news_scraper_pipeline.jp_news_scraper.news_scraper import extract_text_from_url_list, get_unique_urls
from jp_news_scraper_pipeline.jp_news_scraper.sqlite_functions import create_japan_news_table, create_news_url_table, \
    fetch_exist_url_from_db


def get_cleaned_url_list(initial_url):
    """
    Get a cleaned URL list from the initial URL list.
    :param initial_url: An Initial URL list.
    :return: A list of cleaned URL.
    """
    logging.info("Get a cleaned Href list from the initial Href list.")
    initial_urls: list[str] = get_unique_urls(initial_url)
    cleaned_url_list: list[str] = clean_url_list(initial_urls)
    return cleaned_url_list


def get_new_urls(cleaned_url_list, sqlite_db) -> list[str]:
    """
    Get new urls from cleaned URL list.
    :param cleaned_url_list: Cleaned URL list.
    :param sqlite_db: SQLite database.
    :return: New urls as a list.
    """
    logging.info('Get new urls from cleaned URL list.')
    with sqlite3.connect(sqlite_db) as conn:
        create_news_url_table(conn)
        existing_urls: list[str] = fetch_exist_url_from_db(conn)
        new_urls: list[str] = filter_out_urls_existed_in_db(existing_urls, cleaned_url_list)
        process_new_urls(conn, new_urls)
    return new_urls


def transform_data_to_df(kanji_list, pos_list, pos_translated_list) -> pd.DataFrame:
    """
    Transform data into Pandas Dataframe.
    :param kanji_list: Kanji list.
    :param pos_list: Part of Speech list.
    :param pos_translated_list: English translation of Part of Speech list.
    :return: Pandas Dataframe.
    """
    logging.info('Transforming data into Pandas Dataframe...')
    df = create_df_for_japan_news_table(kanji_list, pos_list, pos_translated_list)
    filtered_df = filter_out_pos(df)
    filtered_df = filter_out_non_jp_characters(filtered_df)
    return filtered_df


def extract_data(new_url) -> tuple[list[str], list[str], list[str]]:
    """
    Extract the desired data from the new URL list.
    :param new_url: New URL list.
    :return: Tuple of a Kanji list, Part of Speech list, and English translation of Part of Speech list.
    """
    logging.info('Extracting data from new hrefs list...')
    joined_text_list: list[str] = extract_text_from_url_list(new_url)
    kanji_list: list[str] = extract_kanji(joined_text_list)
    pos_list: list[str] = extract_pos(kanji_list)
    pos_translated_list: list[str] = translate_pos(pos_list)

    list_len: tuple = check_list_len(kanji_list, pos_list, pos_translated_list)
    kanji_list_len = list_len[0]
    logging.debug(f'Kanji list length: {kanji_list_len}')
    pos_list_len = list_len[1]
    logging.debug(f'Part of Speech list length: {pos_list_len}')
    pos_translated_list_len = list_len[2]
    logging.debug(f'Translated Part of Speech list length: {pos_translated_list_len}')

    if kanji_list_len != pos_list_len or kanji_list_len != pos_translated_list_len:
        raise ValueError("The length of kanji_list, pos_list, and pos_translated_list are not equal.")
    else:
        return kanji_list, pos_list, pos_translated_list


def check_list_len(*args) -> tuple:
    """
    Calculate the length of the target list and return it as an integer.
    :param args: Target lists.
    :return: Length of the target list as Tuple.
    """
    logging.info(f"Checking length of target lists...")
    lengths = [len(arg) for arg in args]
    return tuple(lengths)


def load_to_sqlite(filtered_df, sqlite_db) -> None:
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


if __name__ == '__main__':
    pass
