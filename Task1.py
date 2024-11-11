import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

def get_html(url):
    response = requests.get(url)
    return response.text

def get_article_urls(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    urls = [link['href'] for link in links if link['href'].startswith('http')]
    return urls[:5]  # Повертаємо перші 5 URL

def save_article(url, file_name):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(text)

def count_sentences(text):
    sentences = re.split(r'[.!?]', text)
    return len([s for s in sentences if s.strip()])

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_articles(text):
    articles = ['a', 'an', 'the']
    words = re.findall(r'\b\w+\b', text.lower())
    return sum(1 for word in words if word in articles)

def find_prepositions(text):
    prepositions = ['in', 'on', 'at', 'by', 'with', 'about', 'for', 'against', 'during', 'before', 'after']
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if word in prepositions]

base_url = 'https://edition.cnn.com'  # Замість цього ставте базовий URL новинного сайту
article_urls = get_article_urls(base_url)

article_data = []
for i, url in enumerate(article_urls):
    save_article(url, f'article_{i+1}.txt')
    with open(f'article_{i+1}.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        sentences_count = count_sentences(text)
        words_count = count_words(text)
        articles_count = count_articles(text)
        prepositions = find_prepositions(text)
        article_data.append({
            'url': url,
            'sentences_count': sentences_count,
            'words_count': words_count,
            'articles_count': articles_count,
            'prepositions': prepositions,
        })

for data in article_data:
    print(f"URL: {data['url']}")
    print(f"Number of sentences: {data['sentences_count']}")
    print(f"Number of words: {data['words_count']}")
    print(f"Number of articles: {data['articles_count']}")
    print(f"Prepositions in text: {', '.join(data['prepositions'])}")
    print()

words_count = [data['words_count'] for data in article_data]
plt.bar(range(1, 6), words_count)
plt.xlabel('Article Number')
plt.ylabel('Number of Words')
plt.title('Word Count per Article')
plt.show()
