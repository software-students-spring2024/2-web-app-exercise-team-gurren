import pymongo
import bcrypt
import os
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('MONGO_DBNAME')]

# Routes
@app.route('/')
def home():
    # Retrieve recent itineraries from the database
    recent_itineraries = db.destinations.find().sort('_id', -1).limit(5)
    return render_template('home.html', recent_itineraries=recent_itineraries)

@app.route('/search')
def search():
    # Retrieve all destinations from the database
    destinations = [itinerary['destination'] for itinerary in db.destinations.find()]
    return render_template('search.html', destinations=destinations)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get itinerary details from the form
        destination = request.form['destination']
        activities = request.form['activities']
        cost_ratings = request.form['cost_ratings']
        popularity = request.form['popularity']
        
        # Insert the itinerary into the database
        db.destinations.insert_one({
            'destination': destination,
            'activities': activities,
            'cost_ratings (1-5)': cost_ratings,
            'popularity (1-10)': popularity
        })
        
        return redirect(url_for('home'))
    
    # If request method is GET, render the add.html template
    return render_template('add.html')

@app.route('/confirm_delete/<destination>')
def confirm_delete(destination):
    return render_template('confirm_delete.html', destination=destination)


@app.route('/delete/<destination>', methods=['GET', 'POST'])
def delete(destination):
    if request.method == 'POST':
        # Delete the itinerary from the database
        db.destinations.delete_one({'destination': destination})
        return redirect(url_for('home'))
    else:
        # If accessed via GET method, render the confirmation page
        return render_template('confirm_delete.html', destination=destination)

@app.route('/info')
def info():
    # Retrieve all itineraries from the database
    all_itineraries = list(db.destinations.find())
    return render_template('info.html', all_itineraries=all_itineraries)

if __name__ == '__main__':
    app.run(debug=True)
