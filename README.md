# Common Japanese Morphemes in News

Showcase visualizations and code base about the common Japanese morphemes that appear in news.

Morphemes are the smallest units of meaning in a language.

Data was collected from 'https://www3.nhk.or.jp'

Data collecting period: 25th May 2024 - 13th June 2024

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
    ```
- Run the script

### Use Prefect dashboard to monitor the pipeline
- Run ```prefect server start``` in the command line terminal to start a local Prefect server.
- Click the local server link to see the Prefect's dashboard.
  - The link is usually http://127.0.0.1:4200
- Run ```main.py```.
  - You can **monitor only** the **flows** that are **executed** while the **local Prefect server** is **running**. 
    - This includes flows you manually run after starting the local Prefect server.
- For more information, please refer to https://docs.prefect.io/2.10.21/host/
- For more convenience, please use Prefect Cloud.
  - Create a new Prefect Cloud account: https://app.prefect.cloud/?deviceId=54fefa17-9228-4342-aee8-73262fa61a1a
  - Run ```prefect cloud login``` in the terminal.
  - Run the ```main.py``` script.
    - The dashboard can be navigated on Prefect Cloud and Prefect will give you a link to the dashboard when the script 
      is running.
  - More information via this link: https://docs.prefect.io/latest/getting-started/quickstart/

### Set Prefect scheduler
- Run ```prefect server start``` in the command line terminal.
- Go to [scheduler.py](scheduler.py)
- Set the cron parameter as needed.
  ```
  if __name__ == '__main__':
      start_news_scraper_pipeline.serve(
          name='Japan-News-Scraper-Pipeline-Scheduler',
          parameters={"sqlite_db": "japan_news.db", "to_sqlite": True},
          cron='30 14 * * *')  # Adjust the cron parameter as needed
  ```
  - It's set to schedule every day at 9:30 PM as a default.
- Run the script.
- Navigate the Prefect dashboard.
- Navigate the Deployment which you can see the name of the deployed scheduler.
- You **need** to **keep** the **local Prefect server** and ```scheduler.py``` **running** for the **scheduler** to be **online**.
- For more information, please refer to:
  - https://www.prefect.io/blog/schedule-your-code-quickly-with-flow-dot-serve 
  - https://docs.prefect.io/latest/tutorial/deployments/
- If you use Prefect Cloud, a scheduler will be deployed to your Prefect Cloud workspace.
- Ensure that your directory's name doesn't have any space if you want to deploy a Prefect scheduler
  whether it's a local or cloud Prefect server. 

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