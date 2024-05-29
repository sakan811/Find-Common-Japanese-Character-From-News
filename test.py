import sqlite3

import pytest

from japanese_news_scraper import main


def test_main():
    sqlite_db = 'japan_news_test.db'
    main(sqlite_db)

    with sqlite3.connect(sqlite_db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM news')
        rows = c.fetchall()
        assert rows != []


if __name__ == '__main__':
    pytest.main([__file__])
