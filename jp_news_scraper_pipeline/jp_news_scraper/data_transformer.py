import datetime
import re
import sqlite3

import cutlet
import pandas as pd


from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file
from jp_news_scraper_pipeline.jp_news_scraper.utils import get_excluded_jp_pos


logger = configure_logging_with_file(log_file='main.log', logger_name='main', level='INFO')


def romanize_morpheme(morpheme: str) -> str:
    """
    Romanize Japanese morpheme.
    :param morpheme: Morpheme.
    :return: Romanized morpheme.
    """
    return cutlet.Cutlet().romaji(morpheme)


def add_timestamp_to_df(df: pd.DataFrame) -> None:
    """
    Add a timestamp column to the given DataFrame.
    :param df: Pandas DataFrame
    :return: None
    """
    logger.info('Add TimeStamp column to DataFrame')
    df['TimeStamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def clean_url_list(initial_urls: list[str]) -> list[str]:
    """
    Clean the initial href list by excluding unwanted URLs and modifying specific URLs.
    :param initial_urls: Initial URL list.
    :return: A cleaned URL list.
    """
    logger.info('Clean initial href list')
    cleaned_urls = []
    for url in initial_urls:
        if url.startswith('#'):
            continue
        elif url.startswith('https:'):
            continue
        elif url.startswith('//www3.nhk.or.jp'):
            # Extract the path part of the URL
            cleaned_urls.append(url[len('//www3.nhk.or.jp'):])
        else:
            cleaned_urls.append(url)
    return cleaned_urls


def filter_out_urls_existed_in_db(existing_urls: list[str], urls: list[str]) -> list[str]:
    """
    Filter out URLs that are already in the database.
    :param existing_urls: Existing URLs from the database as a list.
    :param urls: URL list.
    :return: Filtered URL list.
    """
    logger.info('Filter out URLs that are already in the database.')
    new_urls = [url for url in urls if url not in existing_urls]

    if not new_urls:
        logger.warning('No new URLs found.')

    return new_urls


def filter_out_non_jp_characters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out non-Japanese characters.
    :param df: Pandas DataFrame.
    :return: Pandas DataFrame.
    """
    logger.info('Filter out non-Japanese characters')
    # Regular expression to match non-Japanese characters (numbers and English words)
    non_japanese_pattern = re.compile(r'[a-zA-Z0-9]')
    # Filter out rows where 'Kanji' contains non-Japanese characters (numbers and English words)
    return df[~df['Kanji'].str.contains(non_japanese_pattern)]


def create_df_for_japan_news_table(
        kanji_list: list[str],
        pos_list: list[str],
        pos_translated_list: list[str]) -> pd.DataFrame:
    """
    Create a dataframe containing data to be inserted into JapanNews table.
    :param kanji_list: Kanji list.
    :param pos_list: Part of Speech list.
    :param pos_translated_list: Translated Part of Speech list.
    :return: Pandas DataFrame.
    """
    logger.info('Create DataFrame with Kanji column')
    df = pd.DataFrame(kanji_list, columns=['Kanji'])
    logger.info('Add Romanji Column')
    df['Romanji'] = df['Kanji'].apply(romanize_morpheme)
    logger.info('Add PartOfSpeech Column')
    df['PartOfSpeech'] = pos_list
    logger.info('Add PartOfSpeechEnglish Column')
    df['PartOfSpeechEnglish'] = pos_translated_list
    add_timestamp_to_df(df)
    return df


def load_new_urls_to_db(conn: sqlite3.Connection, new_urls: list[str]) -> None:
    """
    Load new urls to the SQLite database.
    :param conn: Sqlite3 connection to the database.
    :param new_urls: News URL list.
    :return: None
    """
    logger.info("Loading a new set of news urls into the SQLite database...")
    if new_urls:
        logger.info('Prepare DataFrame for new URLs')
        df = pd.DataFrame(new_urls, columns=['Url'])

        add_timestamp_to_df(df)

        logger.info('Add the DataFrame to NewsUrls table')
        df.to_sql('NewsUrls', conn, if_exists='append', index=False)
    else:
        logger.warning('No new URLs found')


def filter_out_pos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out rows with Part of Speech that needed to be excluded.
    :param df: Pandas dataframe.
    :return: Pandas dataframe.
    """
    logger.info('Filter out rows with Part of Speech that needed to be excluded.')
    excluded_jp_pos_tags = get_excluded_jp_pos()
    return df[~df['PartOfSpeech'].isin(excluded_jp_pos_tags.keys())]
