"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table(
    "restaurant",
    Field("name"),
    Field("city"),
    Field("zipCode", "integer"),
    Field("rating", default=0.0),
    Field("number_of_reviews", default=0),
    Field("cuisine"),
    Field("is_fastfood", default=False)
)

db.define_table(
    'tier_list',
    Field('user_email', default=get_user_email), #user email that added the restaurant
    Field('restaurant_id'), #from db.restaurant.id
    # Field('created_by', 'reference auth_user',
    #       default=lambda: session.user_id),
)

if db(db.restaurant).isempty():
    restaurants = [
        { 
            "name": "Hula\'s Island Grill", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.4,
            "number_of_reviews": 2096,
            "cuisine": "Hawaiian",
            "is_fastfood": False            
        },
        { 
            "name": "Jack\'s Hamburgers", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.5,
            "number_of_reviews": 977,
            "cuisine": "American",
            "is_fastfood": True            
        },
        { 
            "name": "Taqueria Los Pericos", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.6,
            "number_of_reviews": 2096,
            "cuisine": "Mexican",
            "is_fastfood": True            
        },
        { 
            "name": "Jack in the Box", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 3.6,
            "number_of_reviews": 1623,
            "cuisine": "American",
            "is_fastfood": True            
        },
        { 
            "name": "Ideal Bar & Grill", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.0,
            "number_of_reviews": 2317,
            "cuisine": "American",
            "is_fastfood": False            
        }
    ]

    for restaurant in restaurants:
        db.restaurant.insert(name=restaurant['name'],
                             city=restaurant['city'],
                             zipCode=restaurant['zipCode'],
                             rating=restaurant['rating'],
                             number_of_reviews=restaurant['number_of_reviews'],
                             cuisine=restaurant['cuisine'],
                             is_fastfood=restaurant['is_fastfood'])

# db.define_table(
#     "follow",
#     Field("follower", "reference auth_user"),
#     Field("followed", "reference auth_user"),
# )
db.commit()

def add_users_for_testing(num_users):
    # Test user names begin with "_".
    # Counts how many users we need to add.
    #db(db.auth_user.username.startswith("_")).delete()
    num_test_users = 0#db(db.auth_user.username.startswith("_")).count()
    num_new_users = num_users - num_test_users
    print("Adding", num_new_users, "users.")
    for k in range(num_test_users, 5):
        first_name = random.choice(FIRST_NAMES)
        last_name = first_name = random.choice(LAST_NAMES)
        username = "_%s%.2i" % (first_name.lower(), k)
        user = dict(
            username=username,
            email=username + "@ucsc.edu",
            first_name=first_name,
            last_name=last_name,
            password=username,  # To facilitate testing.
        )
        auth.register(user, send=False)
    db.commit()
    
# Comment out this line if you are not interested. 
if db(db.auth_user).isempty():
    add_users_for_testing(5)