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
    rss_url = 'https://services.rechargenews.com/api/feed/rss'

    r = requests.get(rss_url)
    xml = xmltodict.parse(r.content)

    articles = list(pd
                    .DataFrame(xml['rss']['channel']['item'])
                    .pipe(lambda df: df.assign(category=df['category'].apply(lambda cats: ', '.join(cats) if isinstance(cats, list) else cats)))
                    .pipe(lambda df: df.assign(pubDate=pd.to_datetime(df['pubDate']).dt.strftime('%Y-%m-%d %H:%M')))
                    .pipe(lambda df: df.assign(image_filetype=df['media:content'].apply(lambda x: x['@type']).map({'image/jpeg': 'jpg'})))
                    .pipe(lambda df: df.assign(image_url=df['media:content'].apply(lambda x: x['@url'])))
                    .drop(columns=['media:content'])
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