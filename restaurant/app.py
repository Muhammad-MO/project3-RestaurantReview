from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()


load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'Restaurant'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/')
def show_listings():

    country = request.args.get('country')
  
   

    criteria = {}

    if country:
        criteria['cuisine.country'] = country

    listings = db.restaurantname.find(criteria, {
        'name': 1,
        'healthgrade': 1,
        'cuisine': 1,
        'location': 1,
        'images': 1,
        'price': 1,
        'reviews': 1

    }).limit(15)

    return render_template('restaurants.template.html', listings=listings,
                           fullpath=request.full_path)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
