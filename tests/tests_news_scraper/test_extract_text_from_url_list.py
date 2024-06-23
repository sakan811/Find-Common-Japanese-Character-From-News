import pytest

from jp_news_scraper_pipeline.jp_news_scraper.news_scraper import extract_text_from_url_list


# Define test data
@pytest.fixture
def sample_href_list():
    # Sample list of href attributes
    return ['/news/html/20240101/k10013589041000.html', '/news/html/20240101/k10013589042000.html',
            '/news/html/20240101/k10013589042100.html']


# Mocking the requests.get method
class MockResponse:
    def __init__(self, text):
        self.text = text


@pytest.fixture
def mock_requests(monkeypatch):
    def mock_get(url):
        if 'k10013589041000' in url:
            return MockResponse(
                '<html><body><section class="content--detail-main"><div>First article text.</div></section></body></html>')
        elif 'k10013589042000' in url:
            return MockResponse(
                '<html><body><section class="content--detail-main"><div>Second article text.</div></section></body></html>')
        elif 'k10013589042100' in url:
            return MockResponse(
                '<html><body><article class="content--detail-main"><div>Second article text.</div></article></body></html>')
        else:
            raise ValueError("Unexpected URL in test")

    monkeypatch.setattr('requests.get', mock_get)


# Test cases
def test_extract_text_from_url_list_with_articles(sample_href_list, mock_requests):
    # Call the function with sample href attributes
    extracted_texts = extract_text_from_url_list(sample_href_list)

    # Verify that the extracted texts match the content of the news articles
    assert len(extracted_texts) == 2
    assert "First article text." in extracted_texts
    assert "Second article text." in extracted_texts


def test_extract_text_from_url_list_without_articles(sample_href_list, monkeypatch):
    # Empty href list
    empty_href_list = []

    extracted_texts = extract_text_from_url_list(empty_href_list)

    # Verify that no text is extracted
    assert extracted_texts == []
