from bs4 import BeautifulSoup

from jp_news_scraper_pipeline.jp_news_scraper.news_scraper import extract_href_tags


def test_extracts_href_attributes_correctly():
    # Given
    html_content = '<html><body><a href="http://example.com">Example</a></body></html>'
    soup = BeautifulSoup(html_content, 'html.parser')

    # When
    result = extract_href_tags(soup)

    # Then
    assert result == ["http://example.com"]


def test_no_anchor_tags_with_href_attributes():
    # Given
    html_content = '<html><body><p>No links here!</p></body></html>'
    soup = BeautifulSoup(html_content, 'html.parser')

    # Then
    result = extract_href_tags(soup)

    assert result == []


def test_extract_href_tags_with_href_tags_present():
    # Given
    html_content = '''
    <html>
        <body>
            <a href="https://example.com/page1"></a>
            <a href="https://example.com/page2"></a>
        </body>
    </html>
    '''
    mock_soup = BeautifulSoup(html_content, 'html.parser')

    # When
    result = extract_href_tags(mock_soup)

    # Then
    assert result == ['https://example.com/page1', 'https://example.com/page2']


def test_handles_typical_html_with_multiple_anchor_tags():
    # Given
    soup = BeautifulSoup('<a href="https://example.com">Link 1</a><a href="https://example2.com">Link 2</a>',
                         'html.parser')

    # When
    result = extract_href_tags(soup)

    # Then
    assert len(result) == 2
    assert 'https://example.com' in result
    assert 'https://example2.com' in result


def test_no_href_tags_found():
    # Given
    soup = BeautifulSoup('<a></a>', 'html.parser')

    # Then
    result = extract_href_tags(soup)

    assert result == []
