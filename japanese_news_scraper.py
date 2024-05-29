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

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set logging level

# Create a FileHandler with overwritten mode ('w')
file_handler = logging.FileHandler('japan_news.log', mode='w')

# Define a custom log format
log_format = '%(asctime)s | %(filename)s | line:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s'

# Create a Formatter with the custom log format
formatter = logging.Formatter(log_format)

# Set the Formatter for the FileHandler
file_handler.setFormatter(formatter)

# Add the FileHandler to the root logger
logging.getLogger().addHandler(file_handler)


def main(sqlite_db: str) -> None:
    """
    Main function to start a web-scraping process.
    :param sqlite_db: SQLite database file path.
    :return: None
    """
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    data_transformer = DataTransformer()

    initial_hrefs = get_unique_hrefs(initial_url)
    cleaned_href_list = clean_href_list(initial_hrefs)

    with sqlite3.connect(sqlite_db) as conn:
        query = '''
            CREATE TABLE IF NOT EXISTS NewsUrls (
            Url TEXT PRIMARY KEY,
            TimeStamp TEXT
        )
        '''
        conn.execute(query)

        existing_urls = fetch_exist_url_from_db(conn)

        new_hrefs = filter_out_urls_existed_in_db(existing_urls, cleaned_href_list)

        logging.info('Prepare DataFrame for new URLs')
        if new_hrefs:
            df = pd.DataFrame(new_hrefs, columns=['Url'])
            df['TimeStamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.to_sql('NewsUrls', conn, if_exists='append', index=False)

    joined_text_list: list[str] = extract_text_from_href_list(new_hrefs)

    kanji_list = data_transformer.extract_kanji(joined_text_list)

    pos_list = data_transformer.extract_pos(kanji_list)

    pos_translated_list = data_transformer.translate_pos(pos_list)

    df = pd.DataFrame(kanji_list, columns=['Kanji'])
    df['Romanji'] = df['Kanji'].apply(romanize_kanji)
    df['PartOfSpeech'] = pos_list
    df['PartOfSpeechEnglish'] = pos_translated_list
    df['Timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    filtered_df = data_transformer.filter_out_pos(df)

    filtered_df = filter_out_non_jp_characters(filtered_df)

    with sqlite3.connect(sqlite_db) as conn:
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
        filtered_df.to_sql('JapanNews', conn, if_exists='append', index=False)


if __name__ == '__main__':
    sqlite_db = 'japan_news.db'
    main(sqlite_db)
