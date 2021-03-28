from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

#################
#Part I - SCRAPE#
#################

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
    
    ##news_title
    news=soup.find_all("div", class_="content_title")
    ul_item = soup.find('ul', class_= 'item_list')
    li_slide =ul_item.find('li', class_='slide')
    news_title = li_slide.find('div',class_='content_title').text
     
    ##news_p 
    news_p = li_slide.find("div", class_="article_teaser_body").get_text()
     
    ##featured_image_url
    feature_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(feature_url)
    time.sleep(4)
    browser.find_by_css(".btn").click()
    featured_image_url =browser.find_by_css("img.fancybox-image")["src"]
    mars_data["featured_image_url"] = featured_image_url
    
    #Quit Browser - Mars News
    browser.quit()
   
   
    #Facts Table with Pandas 
    path = "https://space-facts.com/mars/"
    table = pd.read_html(path)
    
    ##Load Facts Into Dictionaries List Then DataFrame
    mars_df = table[0]
    
    a=[]
    b=[]
    
    for x in mars_df[0]:
        a.append(x)

    for y in mars_df[1]:
        b.append(y)
    
    fact_table = [
    {"Key": a[0], "Value": b[0]},
    {"Key": a[1], "Value": b[1]},
    {"Key": a[2], "Value": b[3]},
    {"Key": a[4], "Value": b[4]},
    {"Key": a[5], "Value": b[5]},
    {"Key": a[6], "Value": b[6]},
    {"Key": a[7], "Value": b[7]},
    {"Key": a[8], "Value": b[8]},]
   
    ##Format DataFrame into html string
    m = pd.DataFrame(fact_table)
    m.columns = ["Description","Value"]
    m.set_index('Description', inplace=True)
    fact_table = m.to_html()
    
       
    #Mars Hemispheres
    
    ##Request & Hemispheres Names

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    request = requests.get(hemispheres_url)
    s=bs(request.text,"html.parser")
    titles=s.find_all("div", class_="description")
    
    title_list=[]
    
    for g in range(len(titles)):
        title_list.append(titles[g].find("h3").text)

    ##Visit Page 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(h_url)
    
    links_list=[]
    for z in range(len(browser.find_by_css("a.product-item h3"))):
        browser.find_by_css("a.product-item h3")[x].click()
        links_list.append(browser.find_by_css("img.wide-image")["src"])
        browser.back()
    
    ##Quit Browser - Mars Hemispheres
    browser.quit()
    
    h_image_urls = [
    {"title": title_list[0], "img_url": links_list[0]},
    {"title": title_list[1], "img_url": links_list[1]},
    {"title": title_list[2], "img_url": links_list[2]},
    {"title": title_list[3], "img_url": links_list[3]},]
    
    pd.DataFrame(h_image_urls)
    
    
    #Load all scrapped data into 1 object
    mars_data = {
        "news_title":news_title,
        "news_p": news_p,      
        "featured_image":featured_image_url,
        "table":fact_table,
        "hemisphere_image":h_image_urls}
    
    return mars_data


