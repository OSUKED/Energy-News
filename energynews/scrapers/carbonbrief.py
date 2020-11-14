from __future__ import absolute_import

"""
Imports
"""
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

import re
import datetime
from ipypb import track


"""
Categories
"""
def request_CB_category_page(category='science'):
    CB_url = f'https://www.carbonbrief.org/category/{category}'

    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }

    r = requests.get(CB_url, headers=headers)
    
    return r

def extract_topcat(soup):
    topcats = soup.findAll('div', {'class':'ePostC topCat'})
    assert len(topcats) == 1, 'More than one topcat was found'
    topcat = topcats[0]

    article = dict()

    article['date'] = pd.to_datetime(re.sub('\s\s+' , ' ', topcat.find('div', {'class':'dateCat'}).text).strip().replace('.', '')).strftime('%Y-%m-%d')
    article['category'] = topcat.find('div', {'class':'catDate'}).text.split('|')[0].replace('\n', '').strip()
    article['title'] = topcat.find('h3').text.replace('\n', '')
    article['article_url'] = topcat.find('h3').find('a')['href']
    article['image_url'] = topcat.find('img')['src']

    return article

def extract_midcat_data(midcat):
    cat_date = midcat.find('div', {'class':'catDate'})
    category, date = cat_date.text.split('|')

    article = dict()
    
    article['date'] = pd.to_datetime(date.replace('.', '').strip()).strftime('%Y-%m-%d')
    article['category'] = category
    article['title'] = midcat.find('h3').text.replace('\n', '')
    article['article_url'] = midcat.find('h3').find('a')['href']
    article['image_url'] = midcat.find('img')['src']

    return article

def response_to_articles(r):
    articles = list()
    soup = BeautifulSoup(r.content, features='lxml')

    ## Topcat
    topcat_article = extract_topcat(soup)
    articles += [topcat_article]

    ## Midcats
    midcats = soup.findAll('div', {'class':'ePost3'})

    for midcat in midcats:
        midcat_article = extract_midcat_data(midcat)
        articles += [midcat_article]

    ## Bottomcats
    bottomcats = soup.find('div', {'class':'ePostC catSmll'}).findAll('div', {'class':'col-md-6'})

    for bottomcat in bottomcats:
        bottomcat_article = extract_midcat_data(bottomcat)
        articles += [bottomcat_article]
        
    return articles

def retrieve_all_current_articles():
    articles = list()
    sections = ['science', 'energy', 'policy']

    for section in sections:
        r = request_CB_category_page(section)

        section_articles = response_to_articles(r)
        [article.update({'section':section}) for article in section_articles]
        articles += section_articles
        
    return articles


"""
Daily Briefing
"""
def request_CB_daily_brief_page():
    CB_url = f'https://www.carbonbrief.org/daily-brief'

    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }

    r = requests.get(CB_url, headers=headers)
    
    return r

def extract_daily_briefing():
    r = request_CB_daily_brief_page()
    
    content = BeautifulSoup(r.content, features='lxml').find('div', {'class':'innerArt'})
    daily_briefing = dict()
    
    daily_briefing['title'] = content.find('div', {'class': 'miscTitle'}).text.split(' | ')[1].title()
    daily_briefing['headlines'] = [elem.text.replace('\n', ' ') for elem in content.find('div', {'class': 'dailyheadlinesbox'}).findAll('li')]

    return daily_briefing

def daily_briefing_url_to_text():
    daily_briefing = extract_daily_briefing()
    daily_briefing_text = f"{daily_briefing['title']}\n\n* {(chr(10)+'* ').join(daily_briefing['headlines'])}"
    
    return daily_briefing_text


"""
All Articles
"""
def search_CB_articles(page=0, items=100):
    search_url = 'https://www.carbonbrief.org/wp-admin/admin-ajax.php'

    form_data = {
        'currpage' : page,
        'offset' : items,
        'items' : items,
        'layout' : 'large',
        'action' : 'loadmore',
        'allowsorting' : 'true',

    }

    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }

    r = requests.get(search_url, params=form_data, headers=headers)
    
    return r

def search_article_to_data(article_soup):
    article = dict()

    cat_date = article_soup.find('div', {'class':'catDate'})
    cat_dates = cat_date.text.split('|')
    
    if len(cat_dates) >= 2:
        category, date = cat_dates[-2:]
    else:
        category, date = np.nan, cat_dates[0]

    article['date'] = pd.to_datetime(date.replace('.', '-').strip(), format='%d-%m-%y').strftime('%Y-%m-%d')
    article['category'] = category
    article['title'] = article_soup.find('h3').text.replace('\n', '')
    article['article_url'] = article_soup.find('h3').find('a')['href']

    return article

def article_url_to_text(article_url):
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    
    r = requests.get(article_url, headers=headers)
    article_content = BeautifulSoup(r.content).find('div', {'class':'innerArt'}).findAll('p', recursive=False)

    article_text = ''.join([article_content_item.text for article_content_item in article_content if hasattr(re.search('[a-zA-Z0-9_]', article_content_item.text), 'start')])
    article_text = article_text.encode('ascii', 'replace').decode().replace('?', ' ')

    return article_text