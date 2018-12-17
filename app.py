from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")
#What goes in line 10 for the collection?
#Initialize pymongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsapp_db")

# Define database and collection
# db = mongo.marsapp_db
# collection = db.items

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # mars_data = mongo.db.mars_data
    scraped_data = scrape_mars.scrape_info()
    mongo.db.collection.update({}, scraped_data, upsert=True)
    return redirect("/", code=302) #Try with and without code 302


if __name__ == "__main__":
    app.run(debug=True)
