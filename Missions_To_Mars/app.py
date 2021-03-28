from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, redirect, render_template, jsonify
import time
import requests
from flask_pymongo import PyMongo
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

######################
#Part II - PyMONGO DB#
######################

#Initialize Flask
app = Flask(__name__)

#Setup Mongo Connection: Database = Mars_DB, Collection = mars_info

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_DB")

@app.route('/')
def index():
   # Find Data in mars_info Collection
    mars_info = mongo.db.mars_info.find_one()

    # Return template & data
    return render_template("index.html", mars_info=mars_info)

@app.route('/scrape')
def scrape():   
    
    #Scrape New Data & Store In Variable
    mars_data_new = scrape_mars.scrape()
    #Update with new scraped data
    mongo.db.mars_info.update({}, mars_data_new, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)