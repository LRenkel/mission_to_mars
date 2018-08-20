import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

def scrape ():
    mars_facts = {}
    
    nasa_url = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    news_data = requests.get(nasa_url)
    news_data = news_data.json()
    most_recent = news_data.get('items')[0]
    most_recent_body = most_recent['body']
    soup = BeautifulSoup(most_recent_body, "html.parser")
    ps = soup.find_all('p')
    mars_facts['news_p'] = ps[1].get_text()
    mars_facts['news_title'] = most_recent.get('title')

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jpl_page = requests.get(jpl_url)
    soup = BeautifulSoup(jpl_page.text, "html.parser")
    featured_image_url = soup.find("a", {"class":"button fancybox"}).attrs.get('data-fancybox-href')
    mars_facts['featured_image_url'] = f"https://www.jpl.nasa.gov{featured_image_url}"

    twitter = "https://mobile.twitter.com/marswxreport" 
    mars_data = requests.get(twitter)
    soup = BeautifulSoup(mars_data.text, 'html.parser') 
    tweets = soup.find_all("table", {"class": "tweet"})
    tweet_text = [x.find(class_="dir-ltr").get_text() for x in tweets]
    for tweet in tweet_text:
        if tweet.startswith("  Sol"):
            mars_weather = tweet
            break
        else:
            continue
    mars_facts['mars_weather'] = mars_weather.strip()

    marsfacts_url = "https://space-facts.com/mars/"
    marsfacts_table = pd.read_html(marsfacts_url)
    marsfacts_table = marsfacts_table[0]
    mars_facts['marsfacts_table'] = marsfacts_table.to_html()

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_page = requests.get(usgs_url)
    soup = BeautifulSoup(usgs_page.text, "html.parser")
    links = soup.find_all(class_="item")
    links_to_visit = ["https://astrogeology.usgs.gov" + x.contents[0].attrs.get('href') for x in links]
    cerberus = requests.get("https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced")
    soup = BeautifulSoup(cerberus.text, "html.parser")
    divs = soup.find_all("div")
    img_title = divs[0].find("h2", {"class": "title"}).text
    downloads = divs[0].find('div', {"class": "downloads"})
    downloads.find('a').attrs.get('href')
    hemisphere_urls = []
    for link in links_to_visit:
        hemi = requests.get(link)
        soup = BeautifulSoup(hemi.text, "html.parser")
        divs = soup.find_all("div")
        img_title = divs[0].find("h2", {"class": "title"}).text
        downloads = divs[0].find('div', {"class": "downloads"})
        img_url = downloads.find('a').attrs.get('href')
        hemisphere_urls.append({"Title": img_title, "Image_Url": img_url})
    mars_facts['hemisphere_urls'] = hemisphere_urls
    
    return mars_facts