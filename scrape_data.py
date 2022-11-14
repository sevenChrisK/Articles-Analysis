"""Script to scrape the raw articles as input data"""
import time
import requests
from bs4 import BeautifulSoup
from data_access import save_to_db, load_from_db, get_db_keys


def get_article_list():
    """Check if the list of articles already exists in the datastore shelf, if so then return this.
    If the article list does not exist in the shelf then scrape from web and create the datastore."""

    # If script has been run before then articles should already be saved
    # Load the saved articles to prevent unnecessary scraping load on source servers
    if 'articles' in get_db_keys():
        article_list = load_from_db(db_key_string='articles')
        return article_list

    # If script has not been run before / data is not saved then scrape from the internet
    article_list = []

    # Manually checked that there are total 91 pages of articles on university funding
    # TODO create function to return number of pages on a given topic
    for i in range(90):

        page = requests.get(f"https://www.theguardian.com/education/university-funding?page={i + 1}")
        soup = BeautifulSoup(page.text, 'html.parser')

        items = soup.find_all("div", {"class": "fc-item__content"})

        for item in items:
            # get time
            time = item.find("time")['datetime']
            # get link href
            href = item.find("a")['href']
            # get article title, some titles have whitespace so this needs to be stripped
            title = item.find("a").text.strip()

            new_article = {
                "time": time,
                "href": href,
                "title": title
            }

            article_list.append(new_article)

    # Save the scraped data for reuse in future
    save_to_db(db_key_string='articles',
               data_to_save=article_list)

    return article_list
