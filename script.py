import configparser  # for other stuffs :p
import praw  # Python Reddit API Wrapper (The real heart of script)
import requests  # Foboolr Downloading Images
import sys # for argumets
import concurrent.futures  #for multithreading

# fetch api data from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# and using for our praw instance
redditInstance = praw.Reddit(
     client_id=config['apiData']['clientId'],
     client_secret=config['apiData']['clientSecret'],
     user_agent=config['apiData']['userAgent'],
 )
 
# main function to fetch links
stuffLinks = []
def getDankStuffsUrl(whichStuff):
    subReddits= config.get('subReddits', whichStuff)    # getting subreddit from config.ini
    dankStuffs = redditInstance.subreddit(subReddits).random()  # backbone
    if not dankStuffs.is_self: # checking if post has external links or not
        stuffName = dankStuffs.url.split('/')[-1]
        if stuffName.find('.') == -1:   # if this filne name doesn't have any extension get another
            getDankStuffsUrl(whichStuff)
        else:
            stuffLinks.append(dankStuffs.url)  # else append link to the list


# Multithreaded Handler
def gibMeDankStuff(count, whichStuff):
    links = []
    # main thing which handles multi-threads
    with concurrent.futures.ThreadPoolExecutor() as executer:
        [executer.submit(getDankStuffsUrl, whichStuff) for _ in range(count)]   # just run the function getDankStuffsUrl Count number of times "concurrently"
        links =  stuffLinks # I am doing this coz with single list its storing values from previous call. I dunno why
        stuffLinks.clear()  # so I used dirty fix :/
        return links


    
    