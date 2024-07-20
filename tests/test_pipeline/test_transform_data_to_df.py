import pandas as pd

from jp_news_scraper_pipeline.pipeline import transform_data_to_df


def test_transform_data_to_df_correctly(mocker):
    # Given
    kanji_list = ['漢字', '日本', '学校', '勉強']
    pos_list = ['Noun', 'Noun', 'Noun', 'Noun']
    pos_translated_list = ['Noun', 'Noun', 'Noun', 'Noun']

    mocker.patch('jp_news_scraper_pipeline.jp_news_scraper.data_transformer.create_df_for_japan_news_table',
                 return_value=pd.DataFrame({
                     'Kanji': kanji_list,
                     'PartOfSpeech': pos_list,
                     'PartOfSpeechEnglish': pos_translated_list
                 }))
    mocker.patch('jp_news_scraper_pipeline.jp_news_scraper.data_transformer.filter_out_pos', side_effect=lambda df: df)
    mocker.patch('jp_news_scraper_pipeline.jp_news_scraper.data_transformer.filter_out_non_jp_characters',
                 side_effect=lambda df: df)

    # When
    result_df = transform_data_to_df(kanji_list, pos_list, pos_translated_list)

    # Then
    assert not result_df.empty
    assert list(result_df.columns) == ['Kanji', 'Romanji', 'PartOfSpeech', 'PartOfSpeechEnglish', 'TimeStamp']


def test_transform_data_to_df_empty_input(mocker):
    # Given
    kanji_list = []
    pos_list = []
    pos_translated_list = []

    mocker.patch('jp_news_scraper_pipeline.jp_news_scraper.data_transformer.create_df_for_japan_news_table',
                 return_value=pd.DataFrame({
                     'Kanji': kanji_list,
                     'PartOfSpeech': pos_list,
                     'PartOfSpeechEnglish': pos_translated_list
                 }))
    mocker.patch('jp_news_scraper_pipeline.jp_news_scraper.data_transformer.filter_out_pos',
                 side_effect=lambda df: df)
    mocker.patch('jp_news_scraper_pipeline.jp_news_scraper.data_transformer.filter_out_non_jp_characters',
                 side_effect=lambda df: df)

    # When
    result_df = transform_data_to_df(kanji_list, pos_list, pos_translated_list)

    # Then
    assert result_df.empty
