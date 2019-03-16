from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

raw_html = open('GoT Deaths.html').read()  # Open the html file of the GoT deaths page found at https://deathtimeline.com/
html = BeautifulSoup(raw_html, 'html.parser')  # Parse it with BS4

# counter = 0
# for name in html.select('h3'):
#      print(str(counter) +' ' +name.text)
#      counter += 1

data = []

counter = 0  # Counter to see the deathcount
for episode in html.find_all("div", {"class" : "episode-container"}):  # For each episode
    episode_info = episode.find("h3", {"class" : "episode-title"})  # Retrieve the episode info (season, title, episode number)
    episode_info_list = []  # initialize empty list to add individual episode info to

    for item in episode_info:  # For each item (season, episode-title, episode-number)
        episode_info_list.append(item.text)  # Append to the list
        # [0] = Season
        # [1] = episode-title
        # [2] = episode-number

    for name in episode.find_all("div", {"class" : "death-right"}):  # For each name that occurs in the episode
        counter += 1  # Start counting !
        #print(f"{counter}: {name.h3.text} {name.h4.text} in {episode_info_list}.")  # Print the deathcount, character name, how he died, and in what season/episode

        # Create a list of dicts with the information of each characters deaths
        data.append({'death_number' : counter
                    ,'name' : name.h3.text
                    ,'cause_of_death' : name.h4.text
                    ,'died_in_season' : episode_info_list[0]
                    ,'died_in_episode_title' : episode_info_list[1]
                    ,'died_in_episode_number' : episode_info_list[2]})

df = pd.DataFrame(data)  # Make a pandas DataFrame from the list of dicts
column_order = ['death_number', 'name', 'cause_of_death', 'died_in_season', 'died_in_episode_title', 'died_in_episode_number']
df = df[column_order]
df.to_csv('deathlist.csv', index=False)  # Write to CSV

""" extra notes: if you check the page, we can also scrape the episode the character died, time of death etc. """ 