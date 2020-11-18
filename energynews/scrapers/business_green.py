"""
Imports
"""
import pandas as pd

import requests
import xmltodict
from bs4 import BeautifulSoup

from IPython.core.display import JSON


"""
Data Retrieval
"""
def retrieve_all_current_articles():
    rss_url = 'https://www.businessgreen.com/feeds/rss/type/news'

    r = requests.get(rss_url)
    xml = xmltodict.parse(r.content)

    articles = list(pd
                    .DataFrame(xml['rss']['channel']['item'])
                    .pipe(lambda df: df.assign(image_url=df['image'].apply(lambda x: x['url'])))
                    .pipe(lambda df: df.assign(pubDate=pd.to_datetime(df['pubDate']).dt.strftime('%Y-%m-%d %H:%M')))
                    .pipe(lambda df: df.assign(description=df['description'].apply(lambda description: BeautifulSoup(description).get_text()[:250]+'...')))
                    .drop(columns=['image'])
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