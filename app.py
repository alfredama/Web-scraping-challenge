from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    latest_info = mongo.db.scrape_mars.find_one()
    return render_template("index.html", latest_info=latest_info)


@app.route("/scrape")
def scraper():
    latest_data = scrape_mars.scrape()
    mongo.db.scrape_mars.insert_one(latest_data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
