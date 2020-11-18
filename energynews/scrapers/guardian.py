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
def extract_image_filetype(img_url):
    potential_filetypes = ['jpg', 'png']
    
    for filetype in potential_filetypes:
        if filetype in img_url:
            return filetype
        
def retrieve_all_current_articles():
    rss_url = 'https://www.theguardian.com/business/energy-industry/rss'

    r = requests.get(rss_url)
    xml = xmltodict.parse(r.content)

    articles = list(pd
                    .DataFrame(xml['rss']['channel']['item'])
                    .pipe(lambda df: df.assign(category=df['category'].apply(lambda cats: [cat['#text'] for cat in cats]).str.join(', ')))
                    .pipe(lambda df: df.assign(pubDate=pd.to_datetime(df['pubDate']).dt.strftime('%Y-%m-%d %H:%M')))
                    .pipe(lambda df: df.assign(image_url=df['media:content'].apply(lambda x: x[-1]['@url'])))
                    .pipe(lambda df: df.assign(image_filetype=df['image_url'].apply(extract_image_filetype)))
                    .pipe(lambda df: df.assign(description=df['description'].apply(lambda description: BeautifulSoup(description).get_text()[:250]+'...')))
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