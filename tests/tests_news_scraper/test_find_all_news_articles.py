import bs4
import pytest
from bs4 import BeautifulSoup

from jp_news_scraper_pipeline.jp_news_scraper.news_scraper import find_all_news_articles


# Define test data
@pytest.fixture
def sample_inner_soup():
    # Sample HTML content with news articles inside different types of tags
    html_content = """
    <html>
        <body>
            <div class="content--detail-main">
                <p>This is the first news article.</p>
            </div>
            <section class="content--detail-main">
                <div>This is the second news article.</div>
            </section>
            <article class="content--detail-main">
                <div>This is the third news article.</div>
            </article>
            <section class="content--detail-main">
                <div>This is the fourth news article.</div>
            </section>
        </body>
    </html>
    """

    # Parse HTML content into BeautifulSoup object
    inner_soup = BeautifulSoup(html_content, 'html.parser')

    # Return the BeautifulSoup object
    return inner_soup


# Test cases
def test_find_all_news_articles_with_articles(sample_inner_soup):
    # Call the function with the sample BeautifulSoup object
    news_articles = find_all_news_articles(sample_inner_soup)

    # Verify that the function returns a bs4.ResultSet object
    assert isinstance(news_articles, bs4.ResultSet)

    # Verify that the ResultSet contains the expected number of news articles
    assert len(news_articles) == 2

    # Verify that each item in the ResultSet is a section tag with the specified class
    for article in news_articles:
        assert article.name == 'section'
        assert 'content--detail-main' in article['class']


def test_find_all_news_articles_without_articles():
    # Create a BeautifulSoup object without any news articles
    inner_soup = BeautifulSoup("<html><body></body></html>", 'html.parser')

    news_articles = find_all_news_articles(inner_soup)

    assert news_articles is None
