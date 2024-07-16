import datetime
import os

import pandas as pd
from sudachipy import Tokenizer, dictionary, tokenizer

from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file

logger = configure_logging_with_file(log_file='main.log', logger_name='main', level='INFO')


def get_tokenizer() -> Tokenizer:
    """
    Get SudachiPys's tokenizer.
    :return: SudachiPys's tokenizer.
    """
    logger.info("Get SudachiPys's tokenizer.")
    return dictionary.Dictionary().create()


def get_tokenizer_mode() -> Tokenizer.SplitMode:
    """
    Get SudachiPys's tokenizer's mode.
    :return: SudachiPys's tokenizer's mode.
    """
    logger.info("Get SudachiPys's tokenizer's Mode C.")
    return tokenizer.Tokenizer.SplitMode.C


def get_jp_pos_dict():
    """
    Get the Japanese Part of Speech dictionary.
    :return: Japanese Part of Speech dictionary.
    """
    logger.info("Get the Japanese Part of Speech dictionary.")
    return {
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
        "連体詞": "Adnominal",
        "記号": "Symbol"
    }


def get_excluded_jp_pos():
    """
    Get the Japanese Part of Speech that needs to be excluded as a dictionary.
    :return: Excluded Japanese Part of Speech dictionary.
    """
    logger.info("Get the Japanese Part of Speech that needs to be excluded as a dictionary")
    return {
        "空白": "Whitespace",
        "補助記号": "Supplementary Symbol",
        "連体詞": "Adnominal",
        "記号": "Symbol"
    }


def check_if_all_list_len_is_equal(*args) -> bool:
    """
    Check if all list lengths are equal.
    :param args: Target lists.
    :return: True if all list lengths are equal, False otherwise.
    """
    logger.info("Check if all list lengths are equal.")

    list_len: tuple = check_list_len(*args)
    kanji_list_len = list_len[0]
    logger.debug(f'Kanji list length: {kanji_list_len}')
    pos_list_len = list_len[1]
    logger.debug(f'Part of Speech list length: {pos_list_len}')
    pos_translated_list_len = list_len[2]
    logger.debug(f'Translated Part of Speech list length: {pos_translated_list_len}')

    if kanji_list_len == pos_list_len == pos_translated_list_len:
        logger.info("All list lengths are equal.")
        return True
    else:
        logger.info("Not all list lengths are equal.")
        return False


def check_list_len(*args) -> tuple:
    """
    Calculate the length of the target list and return it as an integer.
    :param args: Target lists.
    :return: Length of the target list as Tuple.
    """
    logger.info(f"Checking length of target lists...")
    lengths = [len(arg) for arg in args]
    return tuple(lengths)


def save_data_to_csv(dataframe: pd.DataFrame) -> None:
    """
    Save the data to a CSV file.
    If to_sqlite is set to True, then save data to a local SQLite database, else save it to a CSV file.
    :param dataframe: Pandas Dataframe to be saved.
    :return: None
    """
    logger.info("Saving data as a CSV file...")

    # Create the directory if it does not exist
    directory = 'jp_morphemes_data_from_news'
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
    logger.info('Convert DataFrame to CSV')
    csv_file_path = f'{directory}/jp_words_from_nhk_news_{timestamp}.csv'
    dataframe.to_csv(csv_file_path, index=False)


if __name__ == '__main__':
    pass
