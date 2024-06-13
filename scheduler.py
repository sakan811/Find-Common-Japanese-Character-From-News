from main import start_news_scraper_pipeline


if __name__ == '__main__':
    start_news_scraper_pipeline.serve(
        name='Japan-News-Scraper-Pipeline-Scheduler',
        parameters={"sqlite_db": "japan_news.db", "to_sqlite": True},
        cron='30 14 * * *')