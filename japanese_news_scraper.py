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
import re
import sqlite3

import pandas as pd

from japan_news_scraper.data_transformer import DataTransformer
from japan_news_scraper.news_scraper import NewsScraper

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

if __name__ == '__main__':
    # Main code
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    news_scraper = NewsScraper()
    data_transformer = DataTransformer()

    sqlite_db = 'japan_news.db'

    # Step 1: Get the initial list of unique hrefs from the main news page
    initial_hrefs = news_scraper.get_unique_hrefs(initial_url)
    cleaned_href_list = [href for href in initial_hrefs if not href.startswith('#') and not href.startswith('https:')]

    with sqlite3.connect(sqlite_db) as conn:
        query = '''
            CREATE TABLE IF NOT EXISTS NewsUrls (
            Url TEXT PRIMARY KEY,
            TimeStamp TEXT
        )
        '''
        conn.execute(query)

        # Filter out URLs that already exist in the table
        new_hrefs = data_transformer.filter_new_urls(conn, cleaned_href_list)

        # Prepare DataFrame for new URLs
        if new_hrefs:
            df = pd.DataFrame(new_hrefs, columns=['Url'])
            df['TimeStamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.to_sql('NewsUrls', conn, if_exists='append', index=False)

    joined_text_list: list[str] = news_scraper.extract_text_from_href_list(new_hrefs)

    kanji_list = data_transformer.extract_kanji(joined_text_list)

    pos_list = data_transformer.extract_pos(kanji_list)

    pos_translated_list = data_transformer.translate_pos(pos_list)

    df = pd.DataFrame(kanji_list, columns=['Kanji'])
    df['PartOfSpeech'] = pos_list
    df['PartOfSpeechEnglish'] = pos_translated_list
    df['Timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    filtered_df = df[~df['PartOfSpeech'].isin(data_transformer.excluded_jp_pos_tags.keys())]

    # Regular expression to match non-Japanese characters (numbers and English words)
    non_japanese_pattern = re.compile(r'[a-zA-Z0-9]')

    # Filter out rows where 'Kanji' contains non-Japanese characters (numbers and English words)
    filtered_df = filtered_df[~filtered_df['Kanji'].str.contains(non_japanese_pattern)]

    with sqlite3.connect(sqlite_db) as conn:
        query = '''
        create TABLE IF NOT EXISTS JapanNews (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Kanji TEXT NOT NULL,
            PartOfSpeech TEXT NOT NULL,
            PartOfSpeechEnglish TEXT NOT NULL,
            TimeStamp TEXT NOT NULL
        )
        '''
        conn.execute(query)
        filtered_df.to_sql('JapanNews', conn, if_exists='append', index=False)
