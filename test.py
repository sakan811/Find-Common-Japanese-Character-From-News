import sqlite3

import pytest

from jp_news_scraper_pipeline.configure_logging import configure_logging_with_file
from main import start_news_scraper_pipeline


logger = configure_logging_with_file('test.log', 'test')


def test_main_process():
    sqlite_db = 'japan_news_test.db'
    start_news_scraper_pipeline(sqlite_db, to_sqlite=True)

    with sqlite3.connect(sqlite_db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM JapanNews')
        rows = c.fetchall()
        assert len(rows) > 0

    with sqlite3.connect(sqlite_db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM NewsUrls')
        rows = c.fetchall()
        assert len(rows) > 0


if __name__ == '__main__':
    pytest.main([__file__])
