from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Declare the database
db = client.mars_db
collection = db.mars_data

@app.route("/")
def home():

    # Find data
    mars_data = collection.find_one()

    # return template and data
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    scraped_mars_facts = scrape_mars.scrape()
    #collection.insert_one(scraped_mars_facts)
    collection.update({}, scraped_mars_facts, upsert = True)
    return home()  


if __name__ == "__main__":
    app.run(debug=True, port=5545)

