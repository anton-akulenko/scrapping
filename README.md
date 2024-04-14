## Requirements
 - Just clone the repo and install the requirements using pip install -r requirements.txt
 - Refer to pyproject.toml if you prefer poetry
 - Python >= 3.12.1


## Usage

 - app_url_parser.py will grab urls for news articles 
 - app_articles_scraper.py will grab content from articles (title, author, publication date, content )
 - scrapped data saved as json at  **data** dir

## Project settings
 - Please refer to classes/config.py
 - Replace or add URL's for news articles from websites:
   - 24heures.ch (self.URLS_24HEURES)
   - breakinglatest.news (self.URLS_BREAKINGLATEST)
   - chiswickcalendar.co.uk (self.URLS_CHISWICKCALENDAR)
   - corriere.it (self.URLS_CORRIERE)


#




