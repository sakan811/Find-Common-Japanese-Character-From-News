import sqlite3

import pytest

from main import main


def test_main():
    sqlite_db = 'japan_news_test.db'
    main(sqlite_db)

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
