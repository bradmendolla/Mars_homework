from flask import Flask, render_template
from flask_pymongo import PyMongo
import web_scraping

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb://localhost:27017'
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars_db.find_one()
    return render_template("index.html", mars=mars)