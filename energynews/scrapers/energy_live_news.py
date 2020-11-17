"""
Imports
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


"""
Article Retrieval
"""
def extract_article_data(soup):
    attr_to_extractor_func = {
        'date': lambda soup: '-'.join([str_ for str_ in soup.find('a')['href'].split('/') if str_.isdecimal()]),
        'title': lambda soup: soup.find('div', {'class': 'post-title'}).text,
        'lead': lambda soup: soup.find('div', {'class': 'post-excerpt'}).text.replace('\n', ''),
        'article_url': lambda soup: soup.find('a')['href'],
        'image_url': lambda soup: soup.find('img')['src']
    }
    
    article = dict()
    
    for attr, extractor_func in attr_to_extractor_func.items():
        try:
            article[attr] = extractor_func(soup)
        except:
            pass
    
    return article

def retrieve_all_current_articles():
    url = 'https://www.energylivenews.com/latest-news/'
    r = requests.get(url)

    soup = BeautifulSoup(r.content)
    articles_soup = soup.findAll('div', {'class': 'post-summary row'})

    articles = []

    for article_soup in articles_soup:
        article = extract_article_data(article_soup)
        articles += [article]
        
    return articles