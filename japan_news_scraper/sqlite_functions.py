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


import logging
import sqlite3

import pandas as pd

from .data_transformer import romanize_kanji, fetch_exist_url_from_db, filter_out_urls_existed_in_db, \
    add_timestamp_to_df


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
    pass
