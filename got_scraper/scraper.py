from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

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

counter = 0
for name in html.find_all("div", {"class" : "death-right"}):
    """In the div class 'death-right', we print the h3, which contains the name.
        h4 contains how he died, we want that too"""
    print(f"{counter}: {name.h3.text} {name.h4.text}")
    counter += 1

""" extra notes: if you check the page, we can also scrape the episode the character died, time of death etc. """ 