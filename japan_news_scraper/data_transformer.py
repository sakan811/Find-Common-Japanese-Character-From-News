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
import logging

from sudachipy import Tokenizer, dictionary, tokenizer


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

    def filter_new_urls(self, conn: sqlite3.Connection, urls: list[str]) -> list[str]:
        """
        Filter out URLs that are already in the database.
        :param conn: SQLite 3 connection.
        :param urls: URL list.
        :return: Filtered URL list.
        """
        existing_urls = self.fetch_exist_url_from_db(conn)

        logging.info('Filter out URLs that are already in the database.')
        new_urls = [url for url in urls if url not in existing_urls]

        if not new_urls:
            logging.warning('No new URLs found.')

        return new_urls

    @staticmethod
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
        for word in kanji_list:
            tokenized_word = self.tokenizer_obj.tokenize(word, self.mode)

            # Check if the list is not empty
            if tokenized_word:
                part_of_speech = tokenized_word[0].part_of_speech()

                # Check if part_of_speech is not empty
                if part_of_speech:
                    part_of_speech_list.append(part_of_speech[0])
                else:
                    # Handle case where part_of_speech is empty
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


