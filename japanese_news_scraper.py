import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
from sudachipy import Tokenizer, tokenizer, dictionary


def fetch_and_parse_url(url):
    """Fetch the content of a URL and parse it with BeautifulSoup."""
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def extract_href_tags(soup):
    """Extract all href attributes from anchor tags in the given BeautifulSoup object."""
    href_tags = soup.find_all('a', href=True)
    return [tag['href'] for tag in href_tags]


def get_unique_hrefs(url):
    """Get a list of unique hrefs from the given URL."""
    soup = fetch_and_parse_url(url)
    href_list = extract_href_tags(soup)
    return list(set(href_list))


def crawl_urls(base_url, hrefs):
    """Crawl through each URL in the hrefs list and extract nested hrefs."""
    all_hrefs = set(hrefs)
    for href in hrefs:
        full_url = base_url + href
        nested_hrefs = get_unique_hrefs(full_url)
        all_hrefs.update(nested_hrefs)
    return list(all_hrefs)


def extract_text():
    text_list = []
    for href in cleaned_href_list:
        url = 'https://www3.nhk.or.jp' + href

        # Visit each URL
        inner_response = requests.get(url)
        inner_response.encoding = 'utf-8'
        inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

        # Example: Extract text from paragraph tags
        paragraphs = inner_soup.find_all('section', class_='content--detail-main')

        text_list += append_extracted_text(paragraphs)
    print(text_list)
    return text_list


def append_extracted_text(paragraphs):
    paragraph_list = []
    for paragraph in paragraphs:
        paragraph_list.append(paragraph.text)
    return paragraph_list


if __name__ == '__main__':
    # Main code
    base_url = 'https://www3.nhk.or.jp'
    initial_url = base_url + '/news/'

    # Step 1: Get the initial list of unique hrefs from the main news page
    initial_hrefs = get_unique_hrefs(initial_url)

    # Step 2: Crawl through each initial href to find nested hrefs
    all_hrefs = crawl_urls(base_url, initial_hrefs)

    href_list = list(set(all_hrefs))

    cleaned_href_list = [href for href in href_list if not href.startswith('#') and not href.startswith('https:')]
    joined_text_list = extract_text()

    tokenizer_obj: Tokenizer = dictionary.Dictionary().create()

    mode = tokenizer.Tokenizer.SplitMode.C

    words = []
    for text in joined_text_list:
        words = [m.dictionary_form() for m in tokenizer_obj.tokenize(text, mode)]
    print(words)

    jp_pos_tags = {
        '代名詞': 'Pronoun',
        '副詞': 'Adverb',
        '助動詞': 'Auxiliary verb',
        '助詞': 'Particle',
        '動詞': 'Verb',
        '名詞': 'Noun',
        '形容詞': 'Adjective',
        '形状詞': 'Adjectival noun',
        '感動詞': 'Interjection',
        '接尾辞': 'Suffix',
        '接続詞': 'Conjunction',
        '連体詞': 'Pre-noun adjectival'
    }

    part_of_speech_list = []
    for word in words:
        tokenized_word = tokenizer_obj.tokenize(word, mode)
        if tokenized_word:  # Check if the list is not empty
            part_of_speech = tokenized_word[0].part_of_speech()
            if part_of_speech:  # Check if part_of_speech is not empty
                part_of_speech_list.append(part_of_speech[0])
            else:
                part_of_speech_list.append(None)  # Handle case where part_of_speech is empty
        else:
            part_of_speech_list.append(None)  # Handle case where tokenized_word is empty

    part_of_speech_list = [jp_pos_tags[part_of_speech] for part_of_speech in part_of_speech_list if
                           part_of_speech in jp_pos_tags]

    zipped_data = list(zip(words, part_of_speech_list))

    # Create a DataFrame from the zipped data
    df = pd.DataFrame(zipped_data, columns=['Word', 'Part of Speech'])

    df['Word'] = df['Word'].str.replace(r'[、。「」] = ・ 【 】', '', regex=True)  # Remove unwanted characters
    df = df[df['Word'].str.strip() != '']  # Filter out blank values

    with sqlite3.connect('japan_news.db') as conn:
        df.to_sql('japan_news', conn, if_exists='replace')


