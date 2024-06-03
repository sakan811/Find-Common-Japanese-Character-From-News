import logging

import pandas as pd

from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file
from jp_news_scraper_pipeline.pipeline import transform_data_to_df, extract_data, \
    get_cleaned_url_list, load_to_sqlite, get_new_urls

configure_logging_with_file('japan_news.log')


def start_news_scraper_pipeline(sqlite_db: str) -> None:
    """
    Start a pipeline for web-scraping Japanese news from NHK News.
    :param sqlite_db: SQLite database file path.
    :return: None.
    """
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    cleaned_url_list: list[str] = get_cleaned_url_list(initial_url)

    new_urls: list[str] = get_new_urls(cleaned_url_list, sqlite_db)

    if new_urls:
        kanji_list, pos_list, pos_translated_list = extract_data(new_urls)

        dataframe: pd.DataFrame = transform_data_to_df(kanji_list, pos_list, pos_translated_list)

        load_to_sqlite(dataframe, sqlite_db)
    else:
        logging.warning("No new URL found. Stop the Process.")


if __name__ == '__main__':
    sqlite_db = 'japan_news.db'
    start_news_scraper_pipeline(sqlite_db)
