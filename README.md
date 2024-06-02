# Common Japanese Words in News

Showcase visualizations and code base about the common Japanese words that appear in news.

Data was collected from 'https://www3.nhk.or.jp'

## Status
[![CodeQL](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml)  
[![Python application](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/python-app.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/python-app.yml)  
[![Daily News Scraper](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml)

## Code Base Details

### To web-scrape 'https://www3.nhk.or.jp'
- Go to [main.py](main.py)
- Adjust the SQLite database name as needed
    ```
    sqlite_db = 'japan_news.db' # adjust as needed
    main(sqlite_db)
    ```
- Run the script

### [japan_news_scraper](japan_news_scraper) Package
[data_transformer.py](japan_news_scraper%2Fdata_transformer.py)
- Contain functions and class related to data transformation and cleaning

[news_scraper.py](japan_news_scraper%2Fnews_scraper.py)
- Contain functions related to fetching the data from 'https://www3.nhk.or.jp'

[configure_logging.py](japan_news_scraper%2Fconfigure_logging.py)
- Contain functions about logging configurations.

[sqlite_functions.py](japan_news_scraper%2Fsqlite_functions.py)
- Contain functions related to SQLite database.