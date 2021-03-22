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


@app.route('/restaurants')
def show_listings():

    flavour = request.args.get('flavour')

    criteria = {}

    if flavour:
        criteria['cuisine.flavour'] = flavour

    listings = db.restaurantname.find(criteria, {
        'name': 1,
        'healthgrade': 1,
        'cuisine': 1,
        'ratings': 1,
        'location': 1,
        'images': 1,
        'price': 1,
        'reviews': 1

    }).limit(100)

    return render_template('all_restaurants.template.html', listings=listings,
                           fullpath=request.full_path)


@app.route('/create')
def show_create_restaurant():
    return render_template('create_restaurant.template.html')


@app.route('/create', methods=["POST"])
def process_create_restaurant():
    name = request.form.get('name')
    flavour = request.form.get('flavour')
    ratings = request.form.get('ratings')
    healthgrade = request.form.get('healthgrade')
    Address = request.form.get('Address')
    Country = request.form.get('Country')
    price = request.form.get('price')
    reviews = request.form.get('reviews')

    db.restaurantname.insert_one({
        "name": name,
        "cuisine": {
            "flavour": flavour,
        },
        "ratings": ratings,
        "location": {
            "Address": Address,
            "Country": Country
        },
        "price": price,
        "reviews": reviews
    })

    return redirect(url_for('show_listings'))





if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
