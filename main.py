import argparse
from argparse import Namespace

import pandas as pd
from pandas import DataFrame

from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file
from jp_news_scraper_pipeline.jp_news_scraper.utils import save_data_to_csv
from jp_news_scraper_pipeline.pipeline import transform_data_to_df, extract_data, \
    get_cleaned_url_list, get_new_urls, load_to_sqlite

logger = configure_logging_with_file(log_file='main.log', logger_name='main')


def set_arg_parsers() -> Namespace:
    """
    Set command line arguments.
    :return: Namespace
    """
    parser = argparse.ArgumentParser(description='Parser that control which kind of scraper to use.')
    parser.add_argument('--to_sqlite', type=bool, default=False, help='Save data to SQLite database.')
    return parser.parse_args()


def start_news_scraper_pipeline(sqlite_db: str) -> DataFrame:
    """
    Start a pipeline for web-scraping Japanese news from NHK News.
    :param sqlite_db: SQLite database file path.
    :return: Pandas Dataframe.
    """
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    cleaned_url_list: list[str] = get_cleaned_url_list(initial_url)
    if cleaned_url_list:
        new_urls: list[str] = get_new_urls(cleaned_url_list, sqlite_db)

        if new_urls:
            kanji_list, pos_list, pos_translated_list = extract_data(new_urls)
            return transform_data_to_df(kanji_list, pos_list, pos_translated_list)
        else:
            logger.warning("No new URL found.")
            logger.warning("Return an empty DataFrame.")
            return pd.DataFrame()
    else:
        logger.error("No URL found. Please check the tag in 'extract_href_tags' function in 'news_scraper.py'.")
        logger.warning("Return an empty DataFrame.")
        return pd.DataFrame()


if __name__ == '__main__':
    args = set_arg_parsers()

    # SQLite database is needed.
    # Adjust the database name as needed.
    sqlite_db = 'japan_news.db'
    df = start_news_scraper_pipeline(sqlite_db)
    if not df.empty:
        if args.to_sqlite:
            load_to_sqlite(df, sqlite_db)
        else:
            save_data_to_csv(df)
    else:
        logger.warning("No new URL found. No data was saved. Stop the Process.")

