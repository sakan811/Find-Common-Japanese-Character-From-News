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

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from jp_news_scraper_pipeline.configure_logging import configure_logging
from jp_news_scraper_pipeline.jp_news_scraper.data_extractor import extract_pos, translate_pos
from jp_news_scraper_pipeline.jp_news_scraper.data_transformer import filter_out_non_jp_characters, \
    romanize_kanji, add_timestamp_to_df, filter_out_pos
from jp_news_scraper_pipeline.jp_news_scraper.news_scraper import extract_text_from_url_list
from jp_news_scraper_pipeline.jp_news_scraper.utils import get_tokenizer, get_tokenizer_mode, \
    check_if_all_list_len_is_equal
from jp_news_scraper_pipeline.pipeline import get_cleaned_url_list

configure_logging()


def extract_kanji_from_dict(dictionary: dict) -> pd.DataFrame:
    """
    Extract kanji from the text list.
    :param dictionary: Dictionary where key is HREF and value is its text content.
    :return: DataFrame with HREF as Source and extracted kanji as Kanji columns.
    """
    logging.info('Extract kanji from text list.')
    kanji_data = []
    tokenizer_obj = get_tokenizer()
    mode = get_tokenizer_mode()
    for href, text_list in dictionary.items():
        for text in text_list:
            kanji_list = [m.dictionary_form() for m in tokenizer_obj.tokenize(text, mode)]
            if kanji_list:
                kanji_data.extend([(href, kanji) for kanji in kanji_list])

    if not kanji_data:
        logging.warning('No kanji found.')

    logging.info("Create DataFrame from the kanji data")
    df = pd.DataFrame(kanji_data, columns=['Source', 'Kanji'])
    return df


def daily_news_scraper():
    logging.info("Automated Scraper Function started")

    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    cleaned_url_list: list[str] = get_cleaned_url_list(initial_url)

    joined_text_list = extract_text_from_url_list(cleaned_url_list)
    logging.info("Text extracted from hrefs")

    dictionary = dict(zip(cleaned_url_list, joined_text_list))

    df_with_href_and_kanji = extract_kanji_from_dict(dictionary)
    kanji_list = df_with_href_and_kanji['Kanji'].tolist()
    pos_list = extract_pos(kanji_list)
    pos_translated_list = translate_pos(pos_list)

    is_all_list_len_equal: bool = check_if_all_list_len_is_equal(kanji_list, pos_list, pos_translated_list)

    if not is_all_list_len_equal:
        raise ValueError("The length of kanji_list, pos_list, and pos_translated_list are not equal.")

    logging.info('Romanizing Kanji...')
    df_with_href_and_kanji['Romanji'] = df_with_href_and_kanji['Kanji'].apply(romanize_kanji)
    logging.info('Add PartOfSpeech Column')
    df_with_href_and_kanji['PartOfSpeech'] = pos_list
    logging.info('Add PartOfSpeechEnglish Column')
    df_with_href_and_kanji['PartOfSpeechEnglish'] = pos_translated_list
    add_timestamp_to_df(df_with_href_and_kanji)

    filtered_df = filter_out_pos(df_with_href_and_kanji)
    filtered_df = filter_out_non_jp_characters(filtered_df)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')

    logging.info('Convert DataFrame to Parquet')
    parquet_file_path = f'{timestamp}.parquet'
    # Convert the DataFrame to a Pyarrow Table and write it to a Parquet file
    table = pa.Table.from_pandas(filtered_df)
    pq.write_table(table, parquet_file_path)


daily_news_scraper()
