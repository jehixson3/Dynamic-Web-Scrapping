from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
   executable_path = {'executable_path': 'chromedriver.exe'}
   browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # Create dictionary for scrapped data
    mars_data = {}
    # Visit Mars URL
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)

    # Scrape page into Soup
    html = browser.html
    mars_soup = bs(html, 'html.parser')

    # Get Title and first paragraph from Nasa Website
    news_title = mars_soup.find('div', class_='content_title').text
    news_p = mars_soup.find('div', class_='article_teaser_body').text

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    # Close the browser 

    return mars_data
   
    browser.quit()
   