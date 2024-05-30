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

import functions_framework
from google.cloud import storage

from japan_news_scraper.data_transformer import DataTransformer, clean_href_list, filter_out_non_jp_characters, \
    fetch_exist_url_from_db, filter_out_urls_existed_in_db
from japan_news_scraper.news_scraper import get_unique_hrefs, extract_text_from_href_list
from japanese_news_scraper import create_df_for_japan_news_table, create_news_url_table, process_new_hrefs, \
    create_japan_news_table


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
        if request_json and 'name' in request_json:
            base_url = 'https://www3.nhk.or.jp'
            initial_url = base_url + '/news/'
            sqlite_db = 'gcp_sqlite.db'

            bucket_name = 'gcp_japan_news'

            # Initialize the Google Cloud Storage client
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(sqlite_db)

            if blob.exists():
                # Download the file from GCS if it exists
                logging.info(f"Database {sqlite_db} found in GCS bucket {bucket_name}")
                # Download the file contents into a variable
                sqlite_content = blob.download_as_string()
                logging.info(f"Database {sqlite_db} downloaded from GCS bucket {bucket_name} as variable")
            else:
                logging.info(f"No existing database found in GCS bucket {bucket_name}")
                # Upload the local file to GCS bucket
                blob.upload_from_filename(sqlite_db)
                logging.info(f"Database {sqlite_db} uploaded to GCS bucket {bucket_name}")

            data_transformer = DataTransformer()

            initial_hrefs = get_unique_hrefs(initial_url)
            logging.info(f"Initial hrefs retrieved: {len(initial_hrefs)}")

            cleaned_href_list = clean_href_list(initial_hrefs)
            logging.info(f"Cleaned href list: {len(cleaned_href_list)}")

            with sqlite3.connect(sqlite_db) as conn:
                create_news_url_table(conn)
                existing_urls = fetch_exist_url_from_db(conn)
                new_hrefs = filter_out_urls_existed_in_db(existing_urls, cleaned_href_list)
                logging.info(f"New hrefs to process: {len(new_hrefs)}")
                process_new_hrefs(conn, new_hrefs)

            joined_text_list = extract_text_from_href_list(new_hrefs)
            logging.info("Text extracted from hrefs")

            kanji_list = data_transformer.extract_kanji(joined_text_list)
            pos_list = data_transformer.extract_pos(kanji_list)
            pos_translated_list = data_transformer.translate_pos(pos_list)

            df = create_df_for_japan_news_table(kanji_list, pos_list, pos_translated_list)
            filtered_df = data_transformer.filter_out_pos(df)
            filtered_df = filter_out_non_jp_characters(filtered_df)

            with sqlite3.connect(sqlite_db) as conn:
                create_japan_news_table(conn)
                filtered_df.to_sql('JapanNews', conn, if_exists='append', index=False)
                logging.info("Filtered DataFrame saved to SQLite database")

            # Initialize the Google Cloud Storage client
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(sqlite_db)

            # Upload the file to GCS
            blob.upload_from_filename(sqlite_db)
            logging.info(f"Database uploaded to GCS bucket {bucket_name}")

            return "Database successfully updated and uploaded to GCS", 200
        else:
            logging.error("Request JSON is missing 'name'")
            return "Invalid request", 400
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return "An error occurred during the process", 500
