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

import functions_framework
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google.cloud import storage

from japan_news_scraper.data_transformer import DataTransformer
from japan_news_scraper.news_scraper import NewsScraper


class GcpScraper(NewsScraper):
    def __init__(self):
        super().__init__()

    def extract_text_from_href_list(self, href_list: list[str]) -> dict[str, list[str]]:
        """
        Extract all text from the given href attributes.
        :param href_list: List of href attributes.
        :return: Dictionary of text and its href source.
        """
        logging.info('Extract news articles\' texts from a href list')
        text_dict = {}
        for href in href_list:
            url = 'https://www3.nhk.or.jp' + href

            inner_response = requests.get(url)
            inner_response.encoding = 'utf-8'
            inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

            news_articles = self.find_all_news_articles(inner_soup)

            text_dict[href] = self.append_extracted_text(news_articles)

        if not text_dict:
            logging.warning('No text extracted from the news articles')

        return text_dict


class GcpDataTransformer(DataTransformer):
    def __init__(self):
        self.df = pd.DataFrame(columns=['Kanji', 'Source'])
        super().__init__()

    def extract_kanji(self, text_dict: dict) -> list[str]:
        """
        Extract kanji from the text list.
        :param text_dict: Text dict.
        :return: List of kanji.
        """
        logging.info('Extract kanji from text list.')
        kanji_list = []
        for href, text in text_dict.items():
            if isinstance(text, str):
                words = [m.dictionary_form() for m in self.tokenizer_obj.tokenize(text, self.mode)]
                kanji_list.extend(words)

                for word in words:
                    self.df = self.df.append({'Kanji': word, 'Source': href}, ignore_index=True)
            else:
                logging.warning(f'Invalid text format for {href}. Expected a string.')

        if not kanji_list:
            logging.warning('No kanji found.')

        return kanji_list


def save_dataframe_to_gcs(df, bucket_name, destination_blob_name):
    """
    Saves a DataFrame as a CSV file to Google Cloud Storage.

    :param df: DataFrame to save.
    :param bucket_name: Name of the GCS bucket.
    :param destination_blob_name: Destination path in the GCS bucket.
    """
    # Save the DataFrame to a local CSV file
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    local_file_path = f'gcp_japan_news_scraper_{timestamp}.csv'
    df.to_csv(local_file_path, index=False)

    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file to GCS
    blob.upload_from_filename(local_file_path)

    print(f"File {local_file_path} uploaded to {destination_blob_name} in bucket {bucket_name}.")


@functions_framework.http
def start_gcp_scraper(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    if request_json and 'name' in request_json:
        base_url = 'https://www3.nhk.or.jp'
        initial_url = base_url + '/news/'

        news_scraper = GcpScraper()
        data_transformer = GcpDataTransformer()

        # Get the initial list of unique hrefs from the main news page
        initial_hrefs = news_scraper.get_unique_hrefs(initial_url)
        cleaned_href_list = [href for href in initial_hrefs if
                             not href.startswith('#') and not href.startswith('https:')]

        text_dict: dict = news_scraper.extract_text_from_href_list(cleaned_href_list)

        kanji_list = data_transformer.extract_kanji(text_dict)

        pos_list = data_transformer.extract_pos(kanji_list)

        pos_translated_list = data_transformer.translate_pos(pos_list)

        data_transformer.df['PartOfSpeech'] = pos_list
        data_transformer.df['PartOfSpeechEnglish'] = pos_translated_list
        data_transformer.df['Timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        filtered_df = data_transformer.df[
            ~data_transformer.df['PartOfSpeech'].isin(data_transformer.excluded_jp_pos_tags.keys())]

        # Regular expression to match non-Japanese characters (numbers and English words)
        non_japanese_pattern = re.compile(r'[a-zA-Z0-9]')

        # Filter out rows where 'Kanji' contains non-Japanese characters (numbers and English words)
        filtered_df = filtered_df[~filtered_df['Kanji'].str.contains(non_japanese_pattern)]

        # GCS bucket name and destination blob name
        bucket_name = 'gcp_japan_news'
        destination_blob_name = f'gcp_japan_news_scraper_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

        # Save the DataFrame to GCS
        save_dataframe_to_gcs(filtered_df, bucket_name, destination_blob_name)
