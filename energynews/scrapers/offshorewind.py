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
    rss_url = 'https://www.offshorewind.biz/feed/'

    r = requests.get(rss_url)
    xml = xmltodict.parse(r.content)

    articles = list(pd
                    .DataFrame(xml['rss']['channel']['item'])
                    .pipe(lambda df: df.assign(category=df['category'].str.join(', ')))
                    .pipe(lambda df: df.assign(description=df['description'].str.replace(' [&#8230;]', '')))
                    .pipe(lambda df: df.assign(pubDate=pd.to_datetime(df['pubDate']).dt.strftime('%Y-%m-%d %H:%M')))
                    .rename(columns={
                        'link': 'article_url',
                        'description': 'lead',
                        'image_medium': 'image_url',
                        'pubDate': 'date',
                    })
                    .T
                    .to_dict()
                    .values()
                   )
    
    return articles