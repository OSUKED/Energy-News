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
def retrieve_all_current_articles():
    rss_url = 'http://feeds.greentechmedia.com/GreentechMedia?_ga=2.187898337.813121554.1605616493-1583327211.1605616493'

    r = requests.get(rss_url)
    xml = xmltodict.parse(r.content)

    articles = list(pd
                    .DataFrame(xml['rss']['channel']['item'])
                    .pipe(lambda df: df.assign(pubDate=pd.to_datetime(df['pubDate']).dt.strftime('%Y-%m-%d %H:%M')))
                    .pipe(lambda df: df.assign(image_filetype=df['media:content'].apply(lambda x: x['@type']).map({'image/jpeg': 'jpg', 'image/png': 'png'})))
                    .pipe(lambda df: df.assign(image_url=df['media:content'].apply(lambda x: x['@url'])))
                    .drop(columns=['media:content', 'guid'])
                    .rename(columns={
                        'link': 'article_url',
                        'dc:subject': 'category',
                        'description': 'lead',
                        'pubDate': 'date',
                    })
                    .T
                    .to_dict()
                    .values()
                   )
    
    return articles