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

import sqlite3

import pandas as pd

from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file

logger = configure_logging_with_file('main.log', 'main')


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
    logger.info('Creating NewsUrls table if not exist')
    query = '''
            CREATE TABLE IF NOT EXISTS NewsUrls (
            Url TEXT NOT NULL PRIMARY KEY,
            TimeStamp TEXT NOT NULL
        )
        '''
    conn.execute(query)


def fetch_exist_url_from_db(conn: sqlite3.Connection) -> list[str]:
    """
    Fetch existing URLs from the database.
    :param conn: SQLite 3 connection.
    :return: URL list.
    """
    logger.info('Fetch existing URLs from the database')
    existing_urls_query = 'SELECT Url FROM NewsUrls'
    existing_urls = pd.read_sql_query(existing_urls_query, conn)['Url'].tolist()
    return existing_urls


if __name__ == '__main__':
    pass
