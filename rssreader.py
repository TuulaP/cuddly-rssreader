
import requests
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import numpy as np


## trick to get away of one unneeded warning 
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


# base code from https://practicaldatascience.co.uk/data-science/how-to-read-an-rss-feed-in-python


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)

        # print(response)

        return response

    except requests.exceptions.RequestException as e:
        print(e)



def get_feed(url):
    """Return a Pandas dataframe containing the RSS feed contents.

    Args: 
        url (string): URL of the RSS feed to read.

    Returns:
        df (dataframe): Pandas dataframe containing the RSS feed contents.
    """
    
    response = get_source(url)
    
    df = pd.DataFrame(columns = ['title', 'pubDate', 'guid', 'description'])
   

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            #print("Title:", title)

            pubDate = item.find('pubDate', first=True).text
            guid = item.find('guid', first=True).text
            description = item.find('description', first=True).text

            link = item.find('link', first=True).text

            row = {'title': title, 'pubDate': pubDate, 'guid': guid, 'description': description, 'link': link}
            df = df.append(row, ignore_index=True)



    return df


# TODO get these from external file
urls = """https://devclass.com/feed/
https://practicaldatascience.co.uk/feed.xml"
https://rss.nytimes.com/services/xml/rss/nyt/World.xml
"""

df=pd.DataFrame(np.zeros([1, 3]))
result = []

for feedlink in urls.split("\n"):

    feedlink = feedlink.strip()

    if len(feedlink) <= 5:
        continue

    print("Processing: {}".format(feedlink))

    tempdf = get_feed(feedlink)
    result = pd.concat([df,tempdf])


#df1 = get_feed(url1) 
#df2 = get_feed(url2)
#result = pd.concat([df1, df2])



shortinfo = result[["title", "guid", "pubDate"]]

print(shortinfo)

#for newsitem in shortinfo:
#    print(newsitem['title']) # ['title'], newsitem['guid'])


for index, row in shortinfo.iterrows():
    # print(row)
    title = row["title"]
    row   = row["guid"]
    # dte   = row["pubDate"]   ???

    print('{}, {}'.format(title, row))

## TODO some fancier outputting here


