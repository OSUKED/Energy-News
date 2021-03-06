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
    rss_url = 'https://www.current-news.co.uk/rss'

    r = requests.get(rss_url)
    xml = xmltodict.parse(r.content)

    articles = list(pd
                    .DataFrame(xml['rss']['channel']['item'])
                    .pipe(lambda df: df.assign(enclosure=df['enclosure'].apply(lambda x: x['@url'])))
                    .pipe(lambda df: df.assign(pubDate=pd.to_datetime(df['pubDate']).dt.strftime('%Y-%m-%d %H:%M')))
                    .rename(columns={
                        'link': 'article_url',
                        'description': 'lead',
                        'pubDate': 'date',
                        'source': 'section',
                        'enclosure': 'image_url'
                    })
                    .T
                    .to_dict()
                    .values()
                   )
    
    return articles