#!/usr/bin/env python
# coding: utf-8

# In[85]:


from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    title, article = news()

    post = {
        "title": title,
        "article": article,
        "featured_image": featured_image(),
        "hemispheres": hemispheres(),
        "weather": twitter(),
        "facts": facts()
    }

    browser.quit()
    return post


#get article title and text
def news():
    browser = init_browser()


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_="content_title").get_text()
    article = soup.find('div', class_='article_teaser_body').get_text()
    return title, article



#get image
def featured_image():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    button = browser.find_by_id('full_image')
    button.click()

    more_info = browser.find_link_by_partial_text('more info')

    more_info.click()

    html = browser.html
    soup_img = BeautifulSoup(html, 'html.parser')
    
    img=soup_img.select_one('figure', class_="lede").img.get("src")

    featured_img_url= f'https://www.jpl.nasa.gov{img}'
    featured_img_url
    return featured_img_url

#get weather from twitter
def twitter():

    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # this will not always be accurate, I just kept iterating down the timeline until I got something resembling weather
    # I realize this is hardcoding a solution, but scraping twitter is a nightmare
    mars_weather=print(soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[4].get_text())
    return mars_weather



    #get table of facts
def facts():

    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    facts_df = pd.read_html(url)
    df = facts_df[1]
    df.columns=['Fact', 'Measurement']
    mars_facts = df.to_html()
    return mars_facts

def hemispheres():
# get hemisphere pictures
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []

    links = browser.find_by_css("a.itemLink.product-item h3")

    for x in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.itemLink.product-item h3")[x].click()
        elem = browser.find_link_by_partial_text('Sample').first
        hemisphere['img_url'] = elem['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls, hemisphere