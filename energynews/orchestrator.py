from __future__ import absolute_import

import json
import pandas as pd
from .scrapers import carbonbrief as cb

filepath_to_scraper_func = {
    'carbon_brief': {
        'daily_briefing.json': cb.extract_daily_briefing,
        'current_articles.json': cb.retrieve_all_current_articles,        
    },
}

def scrape_and_save_data(data_dir, filepath_to_scraper_func=filepath_to_scraper_func):
    for source in filepath_to_scraper_func.keys():
        for filename, scraper_func in filepath_to_scraper_func[source].items():
            data = scraper_func()

            with open(f'{data_dir}/{source}/{filename}', 'w') as fp:
                json.dump(data, fp)
                
    return
                
def update_readme_time(readme_fp, 
                       splitter='Last updated: ', 
                       dt_format='%Y-%m-%d %H:%M'):
    
    with open(readme_fp, 'r') as readme:
        txt = readme.read()
    
    start, end = txt.split(splitter)
    old_date = end[:len(dt_format)]
    end = end[len(dt_format):]
    new_date = pd.Timestamp.now().strftime(dt_format)
    
    new_txt = start + splitter + new_date + end
    
    with open(readme_fp, 'w') as readme:
        readme.write(new_txt)
        
    return