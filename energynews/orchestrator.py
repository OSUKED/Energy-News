from __future__ import absolute_import

import json
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