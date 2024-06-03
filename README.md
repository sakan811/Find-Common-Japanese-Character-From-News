# Common Japanese Words in News

Showcase visualizations and code base about the common Japanese words that appear in news.

Data was collected from 'https://www3.nhk.or.jp'

## Status
[![CodeQL](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml)    
[![Scraper Test](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml)  
[![Daily News Scraper](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml)

## Code Base Details

### To web-scrape 'https://www3.nhk.or.jp'
- Go to [main.py](main.py)
- Adjust the SQLite database name as needed
    ```
    sqlite_db = 'japan_news.db' # adjust as needed
    start_news_scraper_pipeline(sqlite_db)
    ```
- Run the script

### [jp_news_scraper_pipeline](jp_news_scraper_pipeline) Package
[pipeline.py](japan_news_scraper%2Fpipeline.py)
- Contain web-scraping pipeline's functions.

[configure_logging.py](japan_news_scraper%2Fconfigure_logging.py)
- Contain functions about logging configurations.

### [jp_news_scraper](jp_news_scraper_pipeline%2Fjp_news_scraper) Package
[news_scraper.py](japan_news_scraper%2Fnews_scraper.py)
- Contain functions related to fetching the data from 'https://www3.nhk.or.jp'

[data_extractor.py](jp_news_scraper_pipeline%2Fjp_news_scraper%2Fdata_extractor.py)
- Contain functions related to extracting data about the Japanese language.

[data_transformer.py](japan_news_scraper%2Fdata_transformer.py)
- Contain functions related to data transformation and cleaning.

[sqlite_functions.py](japan_news_scraper%2Fsqlite_functions.py)
- Contain functions related to SQLite database.

[utils.py](jp_news_scraper_pipeline%2Fjp_news_scraper%2Futils.py)
- Contain utility functions.

## [automated_news_scraper.py](automated_news_scraper.py)
Scrape data from NHK News daily, automated with GitHub Action.