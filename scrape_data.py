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


def filter_articles():
    """Filter out articles that either have non-text content or are
    in directories not allowed for scraping by robots.txt"""
    article_list = get_article_list()

    filters = [
        '/video/',
        '/ng-interactive/',
        '/audio/',
        '/cartoon/',
        '/gallery/',
        '/blog/'
    ]

    filtered_article_list = None

    for filter_string in filters:
        filtered_article_list = [article for article in article_list if filter_string not in article['href']]

    if filtered_article_list is None:
        print("oops, something went wrong here!")
        print("filtered_article_list is None")
        return None

    # Save the updated list for later use
    save_to_db(db_key_string='filtered_articles',
               data_to_save=filtered_article_list)

    return None


def scrape_html_of_articles():
    """Extract the html of each article page in the filtered list of articles,
    save these as soup objects for further refinement"""

    filtered_article_list = load_from_db(db_key_string='filtered_articles')

    for article in filtered_article_list:
        time.sleep(0.5)
        page = requests.get(article['href'])
        soup = BeautifulSoup(page.text, 'html.parser')

        # Storing soup as a string to avoid recursionerror when saving to shelf db
        article['soup'] = f"{soup}"

    # Save the updated list for later use
    save_to_db(db_key_string='filtered_articles',
               data_to_save=filtered_article_list)

    return None


def process_article_raw_html() -> None:
    """Process the raw html to extract relevant information to use in textual analysis"""

    filtered_article_list = load_from_db(db_key_string='filtered_articles')

    for count, article in enumerate(filtered_article_list):
        soup = BeautifulSoup(article['soup'], 'html.parser')

        try:
            standfirst = soup.find("div", {"data-gu-name": "standfirst"}).text
            article['standfirst'] = standfirst
        except Exception as e:
            print(e)
            print(article['href'])
            print(count)

        try:
            maincontent = soup.find("div", {"id": "maincontent"}).text
            article['maincontent'] = maincontent
        except Exception as e:
            print(e)
            print(article['href'])
            print(count)

    # Save the updated list for later use
    save_to_db(db_key_string='filtered_articles',
               data_to_save=filtered_article_list)

    return None
