import argparse
import datetime
import logging
from argparse import Namespace

import pandas as pd

from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file
from jp_news_scraper_pipeline.pipeline import transform_data_to_df, extract_data, \
    get_cleaned_url_list, load_to_sqlite, get_new_urls

configure_logging_with_file('japan_news.log')


def set_arg_parsers() -> Namespace:
    """
    Set command line arguments.
    :return: Namespace
    """
    parser = argparse.ArgumentParser(description='Parser that control which kind of scraper to use.')
    parser.add_argument('--to_sqlite', type=bool, default=False, help='Save data to SQLite database.')
    parser.add_argument('--set_db_name', type=str, default=False, help='Set database\'s name.')
    return parser.parse_args()


def start_news_scraper_pipeline(sqlite_db: str, to_sqlite: bool = False) -> None:
    """
    Start a pipeline for web-scraping Japanese news from NHK News.
    :param sqlite_db: SQLite database file path.
    :param to_sqlite: If True, load data to SQLite database, else save to Parquet.
                    Default is False.
    :return: None.
    """
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    cleaned_url_list: list[str] = get_cleaned_url_list(initial_url)

    new_urls: list[str] = get_new_urls(cleaned_url_list, sqlite_db)

    if new_urls:
        kanji_list, pos_list, pos_translated_list = extract_data(new_urls)

        dataframe: pd.DataFrame = transform_data_to_df(kanji_list, pos_list, pos_translated_list)

        if to_sqlite:
            load_to_sqlite(dataframe, sqlite_db)
        else:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')

            logging.info('Convert DataFrame to CSV')
            csv_file_path = f'jp_words_from_nhk_news_{timestamp}.csv'
            dataframe.to_csv(csv_file_path, index=False)
    else:
        logging.warning("No new URL found. Stop the Process.")


if __name__ == '__main__':
    args = set_arg_parsers()

    # SQLite database is needed.
    # Adjust the database name as needed.
    if args.sset_db_name:
        sqlite_db = args.set_db_name
    else:
        sqlite_db = 'japan_news.db'
    if args.to_sqlite:
        start_news_scraper_pipeline(sqlite_db, to_sqlite=True)
    else:
        start_news_scraper_pipeline(sqlite_db)
