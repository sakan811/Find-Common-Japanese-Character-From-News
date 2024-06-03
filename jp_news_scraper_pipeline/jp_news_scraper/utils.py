import logging

from sudachipy import Tokenizer, dictionary, tokenizer


def get_tokenizer() -> Tokenizer:
    """
    Get SudachiPys's tokenizer.
    :return: SudachiPys's tokenizer.
    """
    logging.info("Get SudachiPys's tokenizer.")
    return dictionary.Dictionary().create()


def get_tokenizer_mode() -> Tokenizer.SplitMode:
    """
    Get SudachiPys's tokenizer's mode.
    :return: SudachiPys's tokenizer's mode.
    """
    logging.info("Get SudachiPys's tokenizer's Mode C.")
    return tokenizer.Tokenizer.SplitMode.C


def get_jp_pos_dict():
    """
    Get the Japanese Part of Speech dictionary.
    :return: Japanese Part of Speech dictionary.
    """
    logging.info("Get the Japanese Part of Speech dictionary.")
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
    logging.info("Get the Japanese Part of Speech that needs to be excluded as a dictionary")
    return {
        "空白": "Whitespace",
        "補助記号": "Supplementary Symbol",
        "連体詞": "Adnominal",
        "記号": "Symbol"
    }


if __name__ == '__main__':
    pass
