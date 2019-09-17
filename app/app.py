from flask import Flask, render_template
from flask_pymongo import PyMongo
import web_scraping

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    mars_db = mongo.db.mars_db.find_one()
    return render_template("index.html")

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars_db
    mars_info = web_scraping.scrape()
    mars.update({}, mars_info, upsert=True)
    return "I think it worked"

if __name__ == "__main__":
    app.run(debug=True)