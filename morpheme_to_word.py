import asyncio
import glob
import json
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import cutlet
import pandas as pd
import unicodedata
from bs4 import BeautifulSoup

from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file
from jp_news_scraper_pipeline.jp_news_scraper.news_scraper import find_all_news_articles, \
    append_extracted_text
from jp_news_scraper_pipeline.jp_news_scraper.utils import get_tokenizer, get_tokenizer_mode

logger = configure_logging_with_file(log_file='convert_morphemes_to_words.log',
                                     logger_name='convert_morphemes_to_words', level="INFO")


def get_jp_dict() -> dict:
    """
    Create a Japanese dictionary from JSON files from JMDict.
    :return: Japanese dictionary
    """
    logger.info("Creating dictionary from JSON files from JMDict...")
    jmdict_dir = 'jmdict_eng'
    word_dict = {}
    # Find all JSON files in the directory
    json_files = glob.glob(os.path.join(jmdict_dir, '*.json'))
    index_json = os.path.join(jmdict_dir, 'index.json')
    tag_bank_json = os.path.join(jmdict_dir, 'tag_bank_1.json')
    filtered_json_files = [json_file for json_file in json_files if
                           json_file != index_json and json_file != tag_bank_json]
    # Iterate through each JSON file
    for json_file in filtered_json_files:
        # Open and read the JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Process each entry in the JSON data
            for entry in data:
                word = entry[0]
                reading = entry[1]
                part_of_speech = entry[2]
                additional_info = entry[3]
                frequency = entry[4]
                meanings = entry[5]
                sequence_number = entry[6]
                tags = entry[7]

                if word not in word_dict:
                    word_dict[word] = []

                word_dict[word].append({
                    "reading": reading,
                    "part_of_speech": part_of_speech,
                    "additional_info": additional_info,
                    "frequency": frequency,
                    "meanings": meanings,
                    "sequence_number": sequence_number,
                    "tags": tags
                })

    return word_dict


def combine_morpheme_to_word(morphemes, dictionary, max_word_length=20):
    """
    Combine morphemes to words by looking at the longest combined morphemes that exist in the dictionary.
    Limit the maximum word length to prevent over-combination.

    :param morphemes: List of morphemes to combine.
    :param dictionary: Japanese dictionary for words lookup.
    :param max_word_length: Maximum allowed length for a combined word.
    :return: List of combined words.
    """
    logger.info("Combining morphemes to words...")
    word_list = []
    pointer1 = 0

    while pointer1 < len(morphemes):
        word_found = False
        # Try the longest possible word starting from pointer1, up to max_word_length
        for pointer2 in range(min(len(morphemes), pointer1 + max_word_length), pointer1, -1):
            word_str = ''.join(morphemes[pointer1:pointer2])
            if word_str in dictionary:
                word_list.append(word_str)
                pointer1 = pointer2
                word_found = True
                break
        if not word_found:
            # If no valid word is found, move pointer 1
            pointer1 += 1

    logger.debug(f"Combined words: {word_list}")
    return word_list


def get_url_list_from_db() -> list:
    """
    Get a list of urls from a database.
    :return: List of urls.
    """
    logger.info('Getting urls from database...')
    with sqlite3.connect('japan_news.db') as con:
        cur = con.cursor()
        result = cur.execute('''select * from NewsUrls''')
        return [row[0] for row in result]


def load_data_to_db(df: pd.DataFrame) -> None:
    """
    Load data into SQLite database.
    :param df: Dataframe with Japanese words data.
    :return: None
    """
    logger.info('Loading data into SQLite database...')
    with sqlite3.connect('japan_news.db') as con:
        query = '''
        Create table if not exists JapaneseWords (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Word TEXT NOT NULL,
            Romanji TEXT NOT NULL,
            PartOfSpeech TEXT NOT NULL
        )
        '''
        con.execute(query)
        con.commit()

    df.to_sql(name='JapaneseWords', con=con, if_exists='replace', index=False)


async def fetch(url: str, session: aiohttp.ClientSession) -> str:
    async with session.get(url) as response:
        response_text = await response.text()
        return response_text


async def extract_text_from_url(href: str, session: aiohttp.ClientSession) -> list[str]:
    url = 'https://www3.nhk.or.jp' + href
    response_text = await fetch(url, session)
    soup = BeautifulSoup(response_text, 'html.parser')
    news_articles = find_all_news_articles(soup)
    if news_articles:
        return append_extracted_text(news_articles)
    return []


async def extract_text_from_url_list_with_async(href_list: list[str]) -> list[str]:
    """
    Extract all text from the given href attributes.
    :param href_list: List of href attributes.
    :return: A list of lists that contain extracted texts.
    """
    logger.info('Extract news articles\' texts from a href list')
    text_list = []

    async with aiohttp.ClientSession() as session:
        tasks = [extract_text_from_url(href, session) for href in href_list]
        results = await asyncio.gather(*tasks)

    for result in results:
        text_list += result

    if not text_list:
        logger.warning('No text extracted from the news articles')

    return text_list


def get_pos_from_word(word_list: list[str], jp_dict: dict) -> list[str]:
    """
    Get Part of Speech from words in the list.
    :param word_list: Word list.
    :param jp_dict: Japanese dictionary for words lookup.
    :return: Part of Speech of each word as a list.
    """
    logger.debug('Getting POS tags from dictionary...')
    pos_list = []
    for word in word_list:
        word_data: dict = jp_dict[word][0]
        word_pos = word_data['part_of_speech']
        pos_list.append(word_pos)

    return pos_list


def extract_morphemes_surface_form(joined_text_list: list[str]) -> list[str]:
    """
    Extract morphemes from the joined texts with surface morpheme form.
    :param joined_text_list: A list of joined text.
    :return: List of Morpheme.
    """
    logger.debug('Extract kanji from text list.')
    words = []
    tokenizer_obj = get_tokenizer()
    mode = get_tokenizer_mode()

    for text in joined_text_list:
        spitted_texts: list[str] = text.split('\n')
        for spitted_text in spitted_texts:
            words += [m.surface() for m in tokenizer_obj.tokenize(spitted_text, mode)]

    if not words:
        logger.warning('No kanji found.')

    return words


def process_chunk(chunk: list[str], jp_dictionary: dict) -> list[pd.DataFrame]:
    """
    Process a chunk of of list of text lists that is divided from the main one.
    :param chunk: A chunk of list of text lists.
    :param jp_dictionary: Japanese dictionary for words lookup.
    :return: List of Dataframe of this chunk.
    """
    logger.info('Processing chunk...')
    df_list_chunk = []

    morpheme_list = extract_morphemes_surface_form(chunk)
    cleaned_morpheme_list = clean_jp_text_list(morpheme_list)

    word_list = combine_morpheme_to_word(cleaned_morpheme_list, jp_dictionary)

    katsu = cutlet.Cutlet()
    romanji_list = [katsu.romaji(word) for word in word_list]

    pos_list = get_pos_from_word(word_list, jp_dictionary)

    df = pd.DataFrame({
        'Word': word_list,
        'Romanji': romanji_list,
        'PartOfSpeech': pos_list
    })

    df_list_chunk.append(df)
    return df_list_chunk


def calculate_chunk_list(text_list: list[str], num_chunk: int) -> list[list[str]]:
    """
    Helper function to divide a list into chunks.
    :param text_list: A list of text.
    :param num_chunk: Number of chunks.
    """
    logger.info('Calculating chunks...')
    chunk_size = len(text_list) // num_chunk
    if chunk_size == 0:
        logger.warning(f'Chunk size is 0. Adjust the chunk size to {len(text_list)}.')
        chunk_size = 2
    return [text_list[i:i + chunk_size] for i in range(0, len(text_list), chunk_size)]


def process_list_of_text_lists_concurrently(
        text_list: list[str],
        jp_dictionary: dict,
        num_chunk: int) -> list[pd.DataFrame]:
    """
    Concurrently process a 'list of text lists' by dividing the list into chunks.
    :param text_list: List of text lists.
    :param jp_dictionary: Japanese dictionary for words lookup.
    :param num_chunk: Number of chunks.
    :return: List of Dataframe.
    """
    logger.info('Processing a list of text lists concurrently...')

    chunks = calculate_chunk_list(text_list, num_chunk)

    df_list = []

    if chunks:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_chunk, chunk, jp_dictionary) for chunk in chunks]
            for future in futures:
                df_list.extend(future.result())

    return df_list


def clean_jp_text_list(text_list):
    """
    Clean a list of Japanese text by removing non-Japanese characters,
    digits, punctuations, and brackets.

    :param text_list: List of strings to clean
    :return: List of cleaned strings
    """
    logger.info("Cleaning morpheme text list...")

    def is_japanese(char):
        return ('CJK' in unicodedata.name(char, '') or
                'HIRAGANA' in unicodedata.name(char, '') or
                'KATAKANA' in unicodedata.name(char, ''))

    cleaned_list = []
    for item in text_list:
        # Remove non-Japanese characters, digits, punctuations, and brackets
        cleaned_item = ''.join(char for char in item if is_japanese(char))
        if cleaned_item:
            cleaned_list.append(cleaned_item)

    return cleaned_list


def clean_pos_in_db() -> None:
    """
    Clean the Part of Speech column in JapaneseWords table.
    :return: None
    """
    logger.info('Cleaning Part of Speech column...')
    with sqlite3.connect('japan_news.db') as connection:
        clean_noun_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Noun'
        where PartOfSpeech glob '[0-9] n*' or PartOfSpeech like 'n%';
        '''
        connection.execute(clean_noun_query)

        clean_verb_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Verb'
        where PartOfSpeech glob '[0-9] v*' or PartOfSpeech like 'v%';
        '''
        connection.execute(clean_verb_query)

        clean_prt_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Particle'
        where PartOfSpeech glob '[0-9] prt*' or PartOfSpeech like 'prt%'
        '''
        connection.execute(clean_prt_query)

        clean_adv_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Adverb'
        where PartOfSpeech glob '[0-9] adv*' or PartOfSpeech like 'adv%'
        '''
        connection.execute(clean_adv_query)

        clean_adj_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Adjective'
        where PartOfSpeech glob '[0-9] adj*' or PartOfSpeech like 'adj%'
        '''
        connection.execute(clean_adj_query)

        clean_exp_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Expression'
        where PartOfSpeech glob '[0-9] exp*' or PartOfSpeech like 'exp%'
        '''
        connection.execute(clean_exp_query)

        clean_conj_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Conjunction'
        where PartOfSpeech glob '[0-9] conj*' or PartOfSpeech like 'conj%'
        '''
        connection.execute(clean_conj_query)

        clean_aux_v_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Auxiliary Verb'
        where PartOfSpeech glob '[0-9] aux-v*' or PartOfSpeech like 'aux-v%'
                or PartOfSpeech like 'aux%' or PartOfSpeech glob '[0-9] aux*'
        '''
        connection.execute(clean_aux_v_query)

        clean_aux_adj_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Auxiliary Adjective'
        where PartOfSpeech glob '[0-9] aux-adj*' or PartOfSpeech like 'aux-adj%'
        '''
        connection.execute(clean_aux_adj_query)

        clean_int_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Interjection'
        where PartOfSpeech glob '[0-9] int*' or PartOfSpeech like 'int%'
        '''
        connection.execute(clean_int_query)

        clean_pronoun_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Pronoun'
        where PartOfSpeech glob '[0-9] pn*' or PartOfSpeech like 'pn%'
        '''
        connection.execute(clean_pronoun_query)

        clean_copula_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Copula'
        where PartOfSpeech glob '[0-9] cop*' or PartOfSpeech like 'cop%'
        '''
        connection.execute(clean_copula_query)

        clean_prefix_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Prefix'
        where PartOfSpeech glob '[0-9] pref*' or PartOfSpeech like 'pref%'
        '''
        connection.execute(clean_prefix_query)

        clean_suffix_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Suffix'
        where PartOfSpeech glob '[0-9] suf*' or PartOfSpeech like 'suf%'
        '''
        connection.execute(clean_suffix_query)

        clean_counter_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Counter'
        where PartOfSpeech glob '[0-9] ctr*' or PartOfSpeech like 'ctr%'
        '''
        connection.execute(clean_counter_query)

        clean_unclassifiled_query = '''
        update JapaneseWords
        set PartOfSpeech = 'Unclassified'
        where PartOfSpeech glob '[0-9] unc*' or PartOfSpeech like 'unc%'
        '''
        connection.execute(clean_unclassifiled_query)

        clean_no_data_query = '''
        update JapaneseWords
        set PartOfSpeech = 'No POS data'
        where PartOfSpeech like ''
        '''
        connection.execute(clean_no_data_query)


if __name__ == '__main__':
    url_list: list[str] = get_url_list_from_db()
    text_list: list[str] = asyncio.run(extract_text_from_url_list_with_async(url_list))

    jp_dictionary = get_jp_dict()

    df_list = process_list_of_text_lists_concurrently(text_list, jp_dictionary, num_chunk=100)

    if df_list:
        main_df = pd.concat(df_list)
        load_data_to_db(main_df)

        clean_pos_in_db()
    else:
        logger.warning('Dataframe list is empty. Stop the process')

