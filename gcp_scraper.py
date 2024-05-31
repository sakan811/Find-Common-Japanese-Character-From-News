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

import functions_framework
import pandas as pd
from flask import Response
from google.cloud import storage

from japan_news_scraper.data_transformer import DataTransformer, clean_href_list, filter_out_non_jp_characters, \
    romanize_kanji
from japan_news_scraper.news_scraper import get_unique_hrefs, extract_text_from_href_list
from japanese_news_scraper import create_df_for_japan_news_table, add_timestamp_to_df


class GcpTransformer(DataTransformer):
    def extract_kanji(self, dictionary: dict) -> pd.DataFrame:
        """
        Extract kanji from the text list.
        :param dictionary: Dictionary where key is HREF and value is its text content.
        :return: DataFrame with HREF as Source and extracted kanji as Kanji columns.
        """
        logging.info('Extract kanji from text list.')
        kanji_data = []

        for href, text_list in dictionary.items():
            for text in text_list:
                kanji_list = [m.dictionary_form() for m in self.tokenizer_obj.tokenize(text, self.mode)]
                if kanji_list:
                    kanji_data.extend([(href, kanji) for kanji in kanji_list])

        if not kanji_data:
            logging.warning('No kanji found.')

        # Create DataFrame from the kanji data
        df = pd.DataFrame(kanji_data, columns=['Source', 'Kanji'])
        return df

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
    logging.info("GCP Scraper Function started")

    try:
        request_json = request.get_json(silent=True)
        if request_json:
            base_url = 'https://www3.nhk.or.jp'
            initial_url = base_url + '/news/'

            data_transformer = DataTransformer()
            gcp_transformer = GcpTransformer()

            initial_hrefs = get_unique_hrefs(initial_url)
            logging.info(f"Initial hrefs retrieved: {len(initial_hrefs)}")

            cleaned_href_list = clean_href_list(initial_hrefs)
            logging.info(f"Cleaned href list: {len(cleaned_href_list)}")

            joined_text_list = extract_text_from_href_list(cleaned_href_list)
            logging.info("Text extracted from hrefs")

            dictionary = dict(zip(cleaned_href_list, joined_text_list))

            df_with_href_and_kanji = gcp_transformer.extract_kanji(dictionary)
            kanji_list = df_with_href_and_kanji['Kanji'].tolist()
            pos_list = data_transformer.extract_pos(kanji_list)
            pos_translated_list = data_transformer.translate_pos(pos_list)

            df_with_href_and_kanji['Romanji'] = df_with_href_and_kanji['Kanji'].apply(romanize_kanji)
            logging.info('Add PartOfSpeech Column')
            df_with_href_and_kanji['PartOfSpeech'] = pos_list
            logging.info('Add PartOfSpeechEnglish Column')
            df_with_href_and_kanji['PartOfSpeechEnglish'] = pos_translated_list
            add_timestamp_to_df(df_with_href_and_kanji)

            filtered_df = data_transformer.filter_out_pos(df_with_href_and_kanji)
            filtered_df = filter_out_non_jp_characters(filtered_df)

            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            bucket_name = 'gcp_japan_news'

            # Convert DataFrame to CSV string
            csv_string = filtered_df.to_csv(index=False)

            # Initialize the Google Cloud Storage client
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)

            # Upload CSV string to GCS
            blob = bucket.blob(f'{timestamp.replace(":", "_")}.csv')
            blob.upload_from_string(csv_string)

            logging.info(f"CSV file uploaded to GCS bucket {bucket_name}")

            return Response("Database successfully updated and uploaded to GCS", status=200)
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return Response("An error occurred during the process", status=500)
