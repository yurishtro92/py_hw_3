from pprint import pprint
import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
KEYWORDS = set(KEYWORDS)

response = requests.get('https://habr.com/ru/all/')
response.raise_for_status()
text = response.text

soup = BeautifulSoup(text, features = 'html.parser')
articles = soup.find_all('article')
hubs = []
names = []
previews_text = []
hubs_names_preview_text = set()
articles_list = []

for article in articles:
    article_hubs = article.find_all('span', class_='tm-article-snippet__hubs-item')
    article_hubs_text = [hub.text.lower() for hub in article_hubs]
    for i in article_hubs_text:
        string = i.split()
        hubs.extend(string)
    hubs = set(hubs)
    hubs_names_preview_text.update(hubs)
    hubs = []

    title = article.find('h2')
    article_names = title.find('span')
    article_name_text = {name.text.lower() for name in article_names}
    for j in article_name_text:
        string = j.split()
        names.extend(string)
    names = set(names)
    hubs_names_preview_text.update(names)
    names = []

    previews = article.find(class_='tm-article-body tm-article-snippet__lead')
    preview_text = previews.find_all('p')
    preview_text_text = {preview.text.lower() for preview in previews}
    for j in preview_text_text:
        string = j.split()
        previews_text.extend(string)
    previews_text = set(previews_text)
    hubs_names_preview_text.update(previews_text)
    previews_text = []

    if KEYWORDS & hubs_names_preview_text:
        title = article.find('h2')
        article_name = title.find('span')
        article_name = article_name.text
        article_link = title.find('a').attrs.get('href')
        url = 'https://habr.com' + article_link
        article_datetime = article.find('time')
        article_date = article_datetime.text
        articles_list.append(article_date)
        articles_list.append(article_name)
        articles_list.append(url)
        articles_list.append('____________')
    hubs_names_preview_text = set()
pprint(articles_list)

