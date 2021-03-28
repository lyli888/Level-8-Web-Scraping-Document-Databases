from flask import Flask, redirect, render_template, jsonify
import time
from flask_pymongo import PyMongo
import scrape_mars

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
    mars_data = scrape_mars.scrape()
    #Update with new scraped data
    mongo.db.mars_info.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)