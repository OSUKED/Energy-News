"""
Imports
"""
import pandas as pd
import requests
import xmltodict
from bs4 import BeautifulSoup


"""
Article Retrieval
"""
def article_url_to_image_url(article_url):
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content)

    image_url = 'https://renews.biz/'+soup.find('div', {'class': 'head-image'}).find('img')['src']

    return image_url

def retrieve_all_current_articles():
    rss_url = 'http://feeds.feedburner.com/Renews-RenewableEnergyNews'

    r = requests.get(rss_url)
    xml = xmltodict.parse(r.content)

    articles = list(pd
                    .DataFrame(xml['rss']['channel']['item'])
                    .pipe(lambda df: df.assign(category=df['category'].str.join(', ')))
                    .pipe(lambda df: df.assign(pubDate=pd.to_datetime(df['pubDate']).dt.strftime('%Y-%m-%d %H:%M')))
                    .pipe(lambda df: df.assign(image_url=df['link'].apply(article_url_to_image_url)))
                    .rename(columns={
                        'link': 'article_url',
                        'description': 'lead',
                        'pubDate': 'date',
                    })
                    .T
                    .to_dict()
                    .values()
                   )
    
    return articles