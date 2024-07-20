import sqlite3

import pandas as pd

from jp_news_scraper_pipeline.pipeline import load_to_sqlite


def test_successfully_saves_dataframe():
    # Given
    data = {
        'Kanji': ['漢字', '日本', '学校', '勉強'],
        'Romanji': ['kanji', 'nippon', 'gakkou', 'benkyou'],
        'PartOfSpeech': ['noun', 'noun', 'noun', 'noun'],
        'PartOfSpeechEnglish': ['Kanji', 'Japan', 'School', 'Study'],
        'TimeStamp': ['2023-10-01 00:00:00', '2023-10-01 00:00:00', '2023-10-01 00:00:00', '2023-10-01 00:00:00']
    }
    df = pd.DataFrame(data)
    sqlite_db = 'test_successfully_saves_dataframe.db'

    # When
    load_to_sqlite(df, sqlite_db)

    # Then
    with sqlite3.connect(sqlite_db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM JapanNews')
        rows = c.fetchall()
        assert len(rows) == 4
        assert rows[0][1] == '漢字'


def test_handles_empty_dataframe():
    # Given
    df = pd.DataFrame(columns=['Kanji', 'Romanji', 'PartOfSpeech', 'PartOfSpeechEnglish', 'TimeStamp'])
    sqlite_db = 'test_handles_empty_dataframe.db'

    # When
    load_to_sqlite(df, sqlite_db)

    # Then
    with sqlite3.connect(sqlite_db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM JapanNews')
        rows = c.fetchall()
        assert len(rows) == 0