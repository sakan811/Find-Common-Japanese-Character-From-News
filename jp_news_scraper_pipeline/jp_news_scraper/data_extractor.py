from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file
from jp_news_scraper_pipeline.jp_news_scraper.utils import get_jp_pos_dict, get_tokenizer, get_tokenizer_mode


logger = configure_logging_with_file(log_file='main.log', logger_name='main')


def extract_kanji(joined_text_list: list[str]) -> list[str]:
    """
    Extract kanji from the text list.
    :param joined_text_list: Text list.
    :return: List of kanji.
    """
    logger.info('Extract kanji from text list.')
    words = []
    tokenizer_obj = get_tokenizer()
    mode = get_tokenizer_mode()
    for text in joined_text_list:
        words += [m.dictionary_form() for m in tokenizer_obj.tokenize(text, mode)]

    if not words:
        logger.warning('No kanji found.')

    return words


def extract_pos(kanji_list: list[str]) -> list[str]:
    """
    Extract Part of Speech from the Kanji list.
    :param kanji_list: Kanji list.
    :return: List of Part of Speech.
    """
    logger.info('Extract Part of Speech from the Kanji list.')
    part_of_speech_list = []
    tokenizer_obj = get_tokenizer()
    mode = get_tokenizer_mode()
    for kanji in kanji_list:
        tokenized_kanji = tokenizer_obj.tokenize(kanji, mode)
        part_of_speech = tokenized_kanji[0].part_of_speech()
        part_of_speech_list.append(part_of_speech[0])

    return part_of_speech_list


def translate_pos(part_of_speech_list: list[str]) -> list[str]:
    """
    Translate Japanese Part of Speech list to English.
    :param part_of_speech_list: Part of Speech list.
    :return: Translated Part of Speech list.
    """
    logger.info('Translate Japanese Part of Speech to English.')
    pos_translated_list = []
    japanese_pos_dict = get_jp_pos_dict()
    for pos in part_of_speech_list:
        translated_pos = japanese_pos_dict[pos]
        pos_translated_list.append(translated_pos)

    return pos_translated_list
