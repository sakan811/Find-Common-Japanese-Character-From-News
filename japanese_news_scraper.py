#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import datetime
import logging
import sqlite3

import pandas as pd

from japan_news_scraper.data_transformer import DataTransformer, romanize_kanji, clean_href_list, \
    filter_out_urls_existed_in_db, \
    filter_out_non_jp_characters, fetch_exist_url_from_db
from japan_news_scraper.news_scraper import get_unique_hrefs, extract_text_from_href_list

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Create a StreamHandler (which outputs to the terminal)
stream_handler = logging.StreamHandler()

# Define a custom log format
log_format = '%(asctime)s | %(filename)s | line:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s'

# Create a Formatter with the custom log format
formatter = logging.Formatter(log_format)

# Set the Formatter for the StreamHandler
stream_handler.setFormatter(formatter)

# Add the StreamHandler to the root logger
logging.getLogger().addHandler(stream_handler)


def main(sqlite_db: str) -> None:
    """
    Main function to start a web-scraping process.
    :param sqlite_db: SQLite database file path.
    :return: None
    """
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    data_transformer = DataTransformer()

    initial_hrefs: list[str] = get_unique_hrefs(initial_url)
    cleaned_href_list: list[str] = clean_href_list(initial_hrefs)

    with sqlite3.connect(sqlite_db) as conn:
        create_news_url_table(conn)
        existing_urls: list[str] = fetch_exist_url_from_db(conn)
        new_hrefs: list[str] = filter_out_urls_existed_in_db(existing_urls, cleaned_href_list)
        process_new_hrefs(conn, new_hrefs)

    joined_text_list: list[str] = extract_text_from_href_list(new_hrefs)

    kanji_list: list[str] = data_transformer.extract_kanji(joined_text_list)

    pos_list: list[str] = data_transformer.extract_pos(kanji_list)

    pos_translated_list: list[str] = data_transformer.translate_pos(pos_list)

    df = create_df_for_japan_news_table(kanji_list, pos_list, pos_translated_list)

    filtered_df = data_transformer.filter_out_pos(df)

    filtered_df = filter_out_non_jp_characters(filtered_df)

    with sqlite3.connect(sqlite_db) as conn:
        create_japan_news_table(conn)
        filtered_df.to_sql('JapanNews', conn, if_exists='append', index=False)


def create_df_for_japan_news_table(
        kanji_list: list[str],
        pos_list: list[str],
        pos_translated_list: list[str]) -> pd.DataFrame:
    """
    Create a dataframe containing data to be inserted into JapanNews table.
    :param kanji_list: Kanji list.
    :param pos_list: Part of Speech list.
    :param pos_translated_list: Translated Part of Speech list.
    :return: Pandas DataFrame.
    """
    logging.info('Create DataFrame with Kanji column')
    df = pd.DataFrame(kanji_list, columns=['Kanji'])
    logging.info('Add Romanji Column')
    df['Romanji'] = df['Kanji'].apply(romanize_kanji)
    logging.info('Add PartOfSpeech Column')
    df['PartOfSpeech'] = pos_list
    logging.info('Add PartOfSpeechEnglish Column')
    df['PartOfSpeechEnglish'] = pos_translated_list
    add_timestamp_to_df(df)
    return df


def process_new_hrefs(conn: sqlite3.Connection, new_hrefs: list[str]) -> None:
    """
    Process new hrefs.
    :param conn: Sqlite3 connection
    :param new_hrefs: News hrefs list
    :return: None
    """
    if new_hrefs:
        logging.info('Prepare DataFrame for new URLs')
        df = pd.DataFrame(new_hrefs, columns=['Url'])

        add_timestamp_to_df(df)

        logging.info('Add the DataFrame to NewsUrls table')
        df.to_sql('NewsUrls', conn, if_exists='append', index=False)
    else:
        logging.warning('No new URLs found')


def add_timestamp_to_df(df: pd.DataFrame) -> None:
    """
    Add timestamp to DataFrame.
    :param df: Pandas DataFrame
    :return: None
    """
    logging.info('Add TimeStamp column to DataFrame')
    df['TimeStamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_japan_news_table(conn: sqlite3.Connection) -> None:
    """
    Create the JapanNews table if not exist.
    :param conn: Sqlite3 connection.
    :return: None
    """
    query = '''
        create TABLE IF NOT EXISTS JapanNews (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Kanji TEXT NOT NULL,
            Romanji TEXT NOT NULL,
            PartOfSpeech TEXT NOT NULL,
            PartOfSpeechEnglish TEXT NOT NULL,
            TimeStamp TEXT NOT NULL
        )
        '''
    conn.execute(query)


def create_news_url_table(conn: sqlite3.Connection) -> None:
    """
    Creates NewsUrls table if not exists.
    :param conn: Sqlite3 connection.
    :return: None
    """
    logging.info('Creating NewsUrls table if not exist')
    query = '''
            CREATE TABLE IF NOT EXISTS NewsUrls (
            Url TEXT NOT NULL PRIMARY KEY,
            TimeStamp TEXT NOT NULL
        )
        '''
    conn.execute(query)


if __name__ == '__main__':
    sqlite_db = 'japan_news.db'
    main(sqlite_db)
