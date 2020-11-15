from __future__ import absolute_import

"""
Imports
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


"""

"""
topic_to_bbc_url = lambda topic: f'https://www.bbc.co.uk/news/topics/{topic}'

def extract_article_data(soup):
    attr_to_extractor_func = {
        'date': lambda soup: pd.to_datetime(soup.find('time').findAll('span')[-1].text).strftime('%Y-%m-%d %H:%M'),
        'title': lambda soup: soup.find('a').text,
        'lead': lambda soup: soup.findAll('p')[-1].text,
        'article_url': lambda soup: 'https://www.bbc.co.uk' + soup.find('a')['href'],
        'image_url': lambda soup: soup.find('img')['src']
    }
    
    article = dict()
    
    for attr, extractor_func in attr_to_extractor_func.items():
        try:
            article[attr] = extractor_func(soup)
        except:
            pass
    
    return article

def response_to_articles(r):
    soup = BeautifulSoup(r.content, features='lxml')
    articles_soup = soup.findAll('article')

    articles = []

    for article_soup in articles_soup:
        article = extract_article_data(article_soup)
        articles += [article]
        
    return articles

def retrieve_all_current_articles(topics=['cdl8n2edl43t/energy-industry', 'cx1m7zg0gpet/renewable-energy']):
    articles = []

    for topic in topics:
        topic_readable = topic.split('/')[1]
        topic_url = topic_to_bbc_url(topic)
        topic_r = requests.get(topic_url)
        topic_articles = response_to_articles(topic_r)

        for article in topic_articles:
            article.update( {'section': topic_readable})

        articles += topic_articles
        
    return articles