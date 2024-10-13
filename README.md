# Common Japanese Morphemes in News

Showcase visualizations and code base about the common Japanese morphemes that appear in news.

Morphemes are the smallest units of meaning in a language.

Data was collected from 'https://www3.nhk.or.jp'

Data collecting period: 25 May 2024 - 4 July 2024

# Status
#### Common Japanese Morphemes in News: 🎉 **Project Completed** 🎉

[![CodeQL](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml)    

[![Scraper Test](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml)  

[![Daily News Scraper](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml)

# Latest Update
**Common Japanese Morphemes in News** Latest Update: 30 July 2024

# Visualizations
[Common Japanese Morphemes in News](#common-japanese-morphemes-in-news):

* Visualizations Latest Update: 13 October 2024

  * [Tableau](https://public.tableau.com/views/jp-news/Top10Morphemes?:language=th-TH&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
  
  * [Instagram](https://www.instagram.com/p/C9A1r-whAog/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

  * [Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0fF7edryCJeqUamiC6me2syJfWq5wAHTBXahTFeZmCseJefevKLLzGioe6ekpvwi6l&id=61553626169836)

# Data
Located in [data](data) folder

## [jp_morpheme_data_from_news_as_of_2024-07-04.parquet](data%2Fjp_morpheme_data_from_news_as_of_2024-07-04.parquet)
Contain Japanese morphemes data collected from the NHK News website.

Total morphemes collected: 1,015,285 

## [news_url_data_from_nhk_as_of_2024-07-04.parquet](data%2Fnews_url_data_from_nhk_as_of_2024-07-04.parquet)
Contain urls which link to the news that the morphemes were collected from.

Total Url collected: 896

Urls in this file should follow https://www3.nhk.or.jp if you want to see the source.

For example: https://www3.nhk.or.jp/news/html/20240523/k10014458551000.html

# How to Web-Scrape Japanese News to Extract Japanese Morphemes 
- Go to [main.py](main.py)
- Adjust the SQLite database name as needed
    ```
    sqlite_db = 'japan_news_test.db' # adjust as needed
    ```
- Run the script

# [automated_news_scraper.py](automated_news_scraper.py)
Scrape data from NHK News daily, automated with GitHub Action.