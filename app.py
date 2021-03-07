from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import pymongo

# we can use ObjectId
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
# assign a secret key to setup sessions
app.secret_key = os.environ.get('SECRET_KEY')

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'Restaurant'



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(
        os.environ.get("PORT")), debug=True)
