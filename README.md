# Table of Contents
- [Status](#status)
- [Latest Update](#latest-update)
- [Common Japanese Morphemes in News](#common-japanese-morphemes-in-news)
- [Common Japanese Words in News](#common-japanese-words-in-news)

# Status
#### Common Japanese Morphemes in News: 🎉 **Project Completed** 🎉

#### Common Japanese Words in News: 🎉 **Project Completed** 🎉

[![CodeQL](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/codeql.yml)    
[![Scraper Test](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/scraper-test.yml)  
[![Daily News Scraper](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml/badge.svg)](https://github.com/sakan811/Find-Common-Japanese-Words-From-News/actions/workflows/daily-news-scraper.yml)

# Latest Update
**Common Japanese Morphemes in News** Latest Update: 16 July 2024

**Common Japanese Words in News** Latest Update: 16 July 2024

# Common Japanese Morphemes in News

Showcase visualizations and code base about the common Japanese morphemes that appear in news.

Morphemes are the smallest units of meaning in a language.

Data was collected from 'https://www3.nhk.or.jp'

Data collecting period: 25 May 2024 - 4 July 2024


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

## Codebase Details

### To web-scrape 'https://www3.nhk.or.jp'
- Go to [main.py](main.py)
- Adjust the SQLite database name as needed
    ```
    sqlite_db = 'japan_news_test.db' # adjust as needed
    ```
- Run the script

### Processes of [main.py](main.py)
1. Fetch the urls which link to news articles in HNK News website.
2. Check whether those urls are already in the database to ensure that the script doesn't scrape texts from the same source twice.
3. Save a new set of urls to the database.
4. Fetch news articles text from those new urls.
5. Extract morphemes, Romanji, and Part of Speech.
6. Clean data and transform them into a Pandas Dataframe.
7. Save data and the news urls to a SQLite database.


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

# Common Japanese Words in News

Showcase visualizations and code base about the common Japanese words that appear in news.

This project was built on top of [Common Japanese Morphemes in News](#common-japanese-morphemes-in-news) project.

Combining morphemes collected from [Common Japanese Morphemes in News](#common-japanese-morphemes-in-news) project into
words by looking them up in the dictionary.

Words that aren't in the dictionary were filtered out.

The Japanese dictionary for word-lookup is based on JMdict: https://github.com/themoeway/jmdict-yomitan

Data collecting period: 25 May 2024 - 4 July 2024

## Visualizations
Visualizations Latest Update: 16 July 2024

[Tableau](https://public.tableau.com/views/JPWordsfromNHKNews/Top10JapaneseWordsfromNewsDashboard?:language=th-TH&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

[Instagram](https://www.instagram.com/p/C9fQMe5sGI4/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid02xBnyAmmdw8hu8YMBxQdzPbnAkYRAWXwMJspkzKwQqaZrHCWLtEeZK1s8BsLdNpAGl&id=61553626169836)


## Data
Located in [data](data) folder

### [jp_word_data_from_news_as_of_2024-07-04.parquet](data%2Fjp_word_data_from_news_as_of_2024-07-04.parquet)
Contain Japanese words data from NHK News.

Total Japanese Words: 426,217

## Codebase Details
[morpheme_to_word.py](morpheme_to_word.py)
- Contain functions that **combine** **Japanese morphemes** to **words**
- You **need** to have **news urls** from **NHK News** **stored** in the **SQLite database** first before running this script.
  - Which means you **should run** [main.py](main.py) to **scrape morphemes** from the **NHK News** first.

### To Combine Morphemes to Words
- Go to [morpheme_to_word.py](morpheme_to_word.py)
- Adjust the SQLite database name to be the same one you used for the [main.py](main.py)
    ```
    sqlite_db = 'japan_news_test.db' # adjust as needed
    ```
- Run [morpheme_to_word.py](morpheme_to_word.py)

### Processes of [morpheme_to_word.py](morpheme_to_word.py)
  1. It fetches the news urls stored in NewsUrls table in the database and scraped the news article.
  2. It extracts morphemes from the articles, clean non-Japanese characters, and combines them into words by looking up
    the words in the dictionary.
  3. Part of Speech and Romanji are added for each word before transform them into a Pandas dataframe.
  4. Load the dataframe into a SQLite database and clean the Part of Speech column.
