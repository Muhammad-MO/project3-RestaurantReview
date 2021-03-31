from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId

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
        "healthgrade": healthgrade,
        "location": {
            "Address": Address,
            "Country": Country
        },
        "price": price,
        "reviews": reviews
    })

    return redirect(url_for('show_listings'))


@app.route('/restaurant/<name_id>/delete')
def delete_restaurant(name_id):
    # find the animal that we want to delete
    Restaurant = db.restaurantname.find_one({
        '_id': ObjectId(name_id)
    })

    return render_template('confirm_delete_restaurant.template.html',
                           restaurant_to_delete=Restaurant)


@app.route('/restaurant/<name_id>/delete', methods=['POST'])
def process_delete_restaurant(name_id):
    db.restaurantname.remove({
        "_id": ObjectId(name_id)
    })
    return redirect(url_for('show_listings'))


@app.route('/restaurant/<name_id>/update')
def update_restaurant(name_id):

    restaurant_to_edit = db.restaurantname.find_one({
        '_id': ObjectId(name_id)
    })

    return render_template('update_restaurant.template.html',
                           restaurant_to_edit=restaurant_to_edit)


@app.route('/restaurant/<name_id>/update', methods=["POST"])
def process_update_restaurant(name_id):
    db.restaurantname.update_one({
        "_id": ObjectId(name_id)

    }, {

        '$set': request.form
    })
    return redirect(url_for('show_listings'))


@app.route('/feedback')
def show_comments():

    criteria = {}

    comments = db.feedback.find(criteria, {
        'name': 1,
        'mobile': 1,
        'restaurant_name': 1,
        'reviews': 1

    }).limit(100)

    return render_template('customer_feedback_template.html',
                           comments=comments, fullpath=request.full_path)


@app.route('/create2')
def show_create_comment():
    return render_template('create_customer_feedback.template.html')


@app.route('/create2', methods=["POST"])
def process_create_comment():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    restaurant_name = request.form.get('restaurant_name')
    reviews = request.form.get('reviews')

    db.feedback.insert({
        "name": name,
        "mobile": mobile,
        "restaurant_name": restaurant_name,
        "reviews": reviews

    })

    return redirect(url_for('show_comments'))


@app.route('/deals')
def show_deals():

    criteria = {}

    offers = db.deals.find(criteria, {
        'name': 1,
        'deals': 1,
        'image': 1

    }).limit(50)
    return render_template('deals_template.html',
                           offers=offers, fullpath=request.full_path)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'), debug=True)