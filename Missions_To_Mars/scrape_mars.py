from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify
import time
import requests
import pymongo 
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def initialize_browser():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    #browser
    browser = initialize_browser()
    mars_data={}
    
    #Mars News
    news_url="https://mars.nasa.gov/news/"
    browser.visit(news_url)    
    html=browser.html
    soup=bs(html,"html.parser")
    
    #news_title
    news=soup.find_all("div", class_="content_title")
    ul_item = soup.find('ul', class_= 'item_list')
    li_slide =ul_item.find('li', class_='slide')
    news_title = li_slide.find('div',class_='content_title').text
    mars_data["news_title"] = news_title
    
    #news_p 
    news_p = li_slide.find("div", class_="article_teaser_body").get_text()
    mars_data["news_p"] = news_p
    
    
    #featured_image_url
    feature_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(feature_url)
    time.sleep(4)
    browser.find_by_css(".btn").click()
    featured_image_url =browser.find_by_css("img.fancybox-image")["src"]
    mars_data["featured_image_url"] = featured_image_url
   
    #Quit browser
    browser.quit()

    
    #Facts Table with Pandas
    path = "https://space-facts.com/mars/"
    table = pd.read_html(path)
    
    


    
    
    #Mars Hemispheres

     
   
    
    #h_LINK
  
    
  
    
    return mars_data