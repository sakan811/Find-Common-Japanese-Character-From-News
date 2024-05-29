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
import re
import sqlite3

import cutlet
import pandas as pd
import logging

from sudachipy import Tokenizer, dictionary, tokenizer


def romanize_kanji(kanji: str) -> str:
    """
    Romanize kanji.
    :param kanji: Kanji.
    :return: Romanized kanji.
    """
    return cutlet.Cutlet().romaji(kanji)


def clean_href_list(initial_hrefs: list[str]) -> list[str]:
    """
    Clean the initial href list by excluding unwanted URLs.
    :param initial_hrefs: Initial href list.
    :return: A cleaned href list.
    """
    logging.info('Clean initial href list')
    return [href for href in initial_hrefs if not href.startswith('#') and not href.startswith('https:')]


def fetch_exist_url_from_db(conn: sqlite3.Connection) -> list[str]:
    """
    Fetch existing URLs from the database.
    :param conn: SQLite 3 connection.
    :return: URL list.
    """
    logging.info('Fetch existing URLs from the database')
    existing_urls_query = 'SELECT Url FROM NewsUrls'
    existing_urls = pd.read_sql_query(existing_urls_query, conn)['Url'].tolist()
    return existing_urls


def filter_out_urls_existed_in_db(existing_urls: list[str], urls: list[str]) -> list[str]:
    """
    Filter out URLs that are already in the database.
    :param existing_urls: Existing URLs from the database as a list.
    :param urls: URL list.
    :return: Filtered URL list.
    """
    logging.info('Filter out URLs that are already in the database.')
    new_urls = [url for url in urls if url not in existing_urls]

    if not new_urls:
        logging.warning('No new URLs found.')

    return new_urls


def filter_out_non_jp_characters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out non-Japanese characters.
    :param df: Pandas DataFrame.
    :return: Pandas DataFrame.
    """
    logging.info('Filter out non-Japanese characters')
    # Regular expression to match non-Japanese characters (numbers and English words)
    non_japanese_pattern = re.compile(r'[a-zA-Z0-9]')
    # Filter out rows where 'Kanji' contains non-Japanese characters (numbers and English words)
    return df[~df['Kanji'].str.contains(non_japanese_pattern)]


class DataTransformer:
    def __init__(self):
        """
        DataTransformer class contains methods related to data transformation.
        """
        self.tokenizer_obj: Tokenizer = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C
        self.japanese_pos_dict = {
            "代名詞": "Pronoun",
            "副詞": "Adverb",
            "助動詞": "Auxiliary Verb",
            "助詞": "Particle",
            "動詞": "Verb",
            "名詞": "Noun",
            "形容詞": "Adjective",
            "形状詞": "Adjectival Noun",
            "感動詞": "Interjection",
            "接尾辞": "Suffix",
            "接続詞": "Conjunction",
            "接頭辞": "Prefix",
            "空白": "Whitespace",
            "補助記号": "Supplementary Symbol",
            "連体詞": "Adnominal"
        }
        self.excluded_jp_pos_tags = {
            "空白": "Whitespace",
            "補助記号": "Supplementary Symbol",
            "連体詞": "Adnominal",
        }

    def extract_kanji(self, joined_text_list: list[str]) -> list[str]:
        """
        Extract kanji from the text list.
        :param joined_text_list: Text list.
        :return: List of kanji.
        """
        logging.info('Extract kanji from text list.')
        words = []
        for text in joined_text_list:
            words = [m.dictionary_form() for m in self.tokenizer_obj.tokenize(text, self.mode)]

        if not words:
            logging.warning('No kanji found.')

        return words

    def extract_pos(self, kanji_list: list[str]) -> list[str]:
        """
        Extract Part of Speech from the Kanji list.
        :param kanji_list: Kanji list.
        :return: List of Part of Speech.
        """
        logging.info('Extract Part of Speech from the Kanji list.')
        part_of_speech_list = []
        for kanji in kanji_list:
            tokenized_kanji = self.tokenizer_obj.tokenize(kanji, self.mode)

            # Check if the list is not empty
            if tokenized_kanji:
                part_of_speech = tokenized_kanji[0].part_of_speech()

                # Check if part_of_speech is not empty
                if part_of_speech:
                    part_of_speech_list.append(part_of_speech[0])
                else:
                    # Handle a case where part_of_speech is empty
                    part_of_speech_list.append(None)
            else:
                # Handle case where tokenized_word is empty
                part_of_speech_list.append(None)

        return part_of_speech_list

    def translate_pos(self, part_of_speech_list: list[str]) -> list[str]:
        """
        Translate Japanese Part of Speech list to English.
        :param part_of_speech_list: Part of Speech list.
        :return: Translated Part of Speech list.
        """
        pos_translated_list = []
        for pos in part_of_speech_list:
            translated_pos = self.japanese_pos_dict[pos]
            pos_translated_list.append(translated_pos)

        return pos_translated_list

    def filter_out_pos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out rows with Part of Speech that needed to be excluded.
        :param df: Pandas dataframe.
        :return: Pandas dataframe.
        """
        logging.info('Filter out rows with Part of Speech that needed to be excluded.')
        return df[~df['PartOfSpeech'].isin(self.excluded_jp_pos_tags.keys())]
