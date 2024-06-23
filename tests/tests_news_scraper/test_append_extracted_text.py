import pytest
from bs4 import BeautifulSoup

from jp_news_scraper_pipeline.jp_news_scraper.news_scraper import append_extracted_text


# Define test data
@pytest.fixture
def sample_news_articles():
    # Sample HTML content of news articles
    html_content1 = "<div>This is the first news article.</div>"
    html_content2 = "<div>This is the second news article.</div>"

    # Parse HTML content into BeautifulSoup objects
    article1 = BeautifulSoup(html_content1, 'html.parser')
    article2 = BeautifulSoup(html_content2, 'html.parser')

    # Return a list of BeautifulSoup objects representing news articles
    return [article1, article2]


# Test cases
def test_append_extracted_text(sample_news_articles):
    # Call the function with sample news articles
    extracted_texts = append_extracted_text(sample_news_articles)

    # Verify that the extracted_texts list contains the expected number of items
    assert len(extracted_texts) == 2

    # Verify that each item in the extracted_texts list is a string
    for text in extracted_texts:
        assert isinstance(text, str)

    # Verify that the extracted text matches the content of the news articles
    assert "This is the first news article." in extracted_texts[0]
    assert "This is the second news article." in extracted_texts[1]
