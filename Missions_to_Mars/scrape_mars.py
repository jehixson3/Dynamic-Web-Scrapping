from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

# Create dictionary for scrapped data
mars_data = {}

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars URL
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)

    # Scrape page into Soup
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')

    # Get Title and first paragraph from Nasa Website
    news_title = mars_soup.find('div', class_='content_title').text
    news_p = mars_soup.find('div', class_='article_teaser_body').text
    

    # Put in dictionary
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    
    # URL to page to be scrapped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Click on full image
    browser.click_link_by_partial_text('FULL IMAGE')

    # Add sleep between clicks
    time.sleep(5)

    # Click on more info
    browser.click_link_by_partial_text('more info') 

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Scrape URL
    img_url = img_soup.find('figure', class_='lede').a['href']
    img_full_url = f'https://www.jpl.nasa.gov{img_url}'

    mars_data["img_full_urll"] = img_full_url

    # Mars weather tweets
    # URL to be scrapped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # put html into BS
    html = browser.html
    twt_soup = BeautifulSoup(html, 'html.parser')

    # Get tweet from BS
    f_twt = twt_soup.find('p', class_='js-tweet-text').text
    mrs_wthr_twt = f_twt.strip()

    mars_data["mrs_wthr_twt"] = mrs_wthr_twt

    # Go to URL and scrap Mars Facts
    url = "https://space-facts.com/mars/"

    mars_fact = pd.read_html(url)
    mars_df = mars_fact[0]

    # Rename Columns
    mars_df.columns = ['Fact', 'Value']

    # convert data frame to html
    data = mars_df.to_html('mars_facts.html')

    mars_data["mars_fact"] = data


    # Mars Hemishperes
    # URL of page to be scrapped
    hemisph_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisph_url)

    # Put html in BS 
    hemisph_html = browser.html
    hemisph_soup = BeautifulSoup(hemisph_html, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = hemisph_soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisph_image_urls = []

    # Store the main_ul 
    hemisph_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemisph_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup(partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemisph_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        hemisph_image_urls.append({"Title" : title, "Img_url" : img_url})

        mars_data["hemisphere_image_url"] = hemisph_image_urls

    # Close the browser 
        browser.quit()

        return mars_data
   
   