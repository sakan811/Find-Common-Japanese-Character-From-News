# Common Japanese Morphemes in News

Showcase visualizations and code base about the common Japanese morphemes that appear in news.

Morphemes are the smallest units of meaning in a language.

Data was collected from 'https://www3.nhk.or.jp'

Data collecting period: 25 May 2024 - 4 July 2024

## Status
Project Latest Update: 5 July 2024

[![CodeQL](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml)    
[![Scraper Test](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml)  
[![Daily News Scraper](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml)


## Visualizations
Visualizations Latest Update: 5 July 2024

[Tableau](https://public.tableau.com/views/jp-news/Top10Morphemes?:language=th-TH&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

[Instagram](https://www.instagram.com/p/C9A1r-whAog/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0fF7edryCJeqUamiC6me2syJfWq5wAHTBXahTFeZmCseJefevKLLzGioe6ekpvwi6l&id=61553626169836)

## Data
Located in [data](data) folder

### [jp_morpheme_data_from_news_as_of_2024-07-04.parquet](data%2Fjp_morpheme_data_from_news_as_of_2024-07-04.parquet)
Contain Japanese morphemes data collected from the NHK News website.

Total morphemes collected: 1,015,285 

### [news_url_data_from_nhk_as_of_2024-07-04.parquet](data%2Fnews_url_data_from_nhk_as_of_2024-07-04.parquet)
Contain urls which link to the news that the morphemes were collected from.

Total Url collected: 896

Urls in this file should follow https://www3.nhk.or.jp if you want to see the source.

For example: https://www3.nhk.or.jp/news/html/20240523/k10014458551000.html

## Code Base Details

### To web-scrape 'https://www3.nhk.or.jp'
- Go to [main.py](main.py)
- Adjust the SQLite database name as needed
    ```
    sqlite_db = 'japan_news.db' # adjust as needed
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
