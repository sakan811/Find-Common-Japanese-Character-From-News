from japan_news_scraper.configure_logging import configure_logging_with_file
from japan_news_scraper.data_transformer import DataTransformer, clean_href_list, filter_out_non_jp_characters
from japan_news_scraper.sqlite_functions import create_df_for_japan_news_table, migrate_to_sqlite, get_new_urls
from japan_news_scraper.news_scraper import get_unique_hrefs, extract_text_from_href_list

configure_logging_with_file('japan_news.log')


def main(sqlite_db: str) -> None:
    """
    Main function to start a web-scraping process.
    :param sqlite_db: SQLite database file path.
    :return: None.
    """
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    data_transformer = DataTransformer()

    initial_hrefs: list[str] = get_unique_hrefs(initial_url)
    cleaned_href_list: list[str] = clean_href_list(initial_hrefs)

    new_hrefs = get_new_urls(cleaned_href_list, sqlite_db)

    joined_text_list: list[str] = extract_text_from_href_list(new_hrefs)

    kanji_list: list[str] = data_transformer.extract_kanji(joined_text_list)

    pos_list: list[str] = data_transformer.extract_pos(kanji_list)

    pos_translated_list: list[str] = data_transformer.translate_pos(pos_list)

    df = create_df_for_japan_news_table(kanji_list, pos_list, pos_translated_list)

    filtered_df = data_transformer.filter_out_pos(df)

    filtered_df = filter_out_non_jp_characters(filtered_df)

    migrate_to_sqlite(filtered_df, sqlite_db)


if __name__ == '__main__':
    sqlite_db = 'japan_news.db'
    main(sqlite_db)
