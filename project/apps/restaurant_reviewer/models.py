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
        },
        { 
            "name": "Poke House", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.3,
            "number_of_reviews": 247,
            "cuisine": "Hawaiian Fusion",
            "is_fastfood": True            
        },
        { 
            "name": "The Poke Bowl", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.3,
            "number_of_reviews": 156,
            "cuisine": "Hawaiian Fusion",
            "is_fastfood": True            
        },
        { 
            "name": "Sabieng Thai Cuisine", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.4,
            "number_of_reviews": 399,
            "cuisine": "Thai",
            "is_fastfood": False            
        },
        { 
            "name": "Real Thai Kitchen", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.1,
            "number_of_reviews": 317,
            "cuisine": "Thai",
            "is_fastfood": False            
        },
        { 
            "name": "Royal Taj India Cuisine", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.2,
            "number_of_reviews": 239,
            "cuisine": "Indian",
            "is_fastfood": False            
        },
        { 
            "name": "L & L Hawaiian Barbeque", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.1,
            "number_of_reviews": 596,
            "cuisine": "Hawaiian",
            "is_fastfood": True            
        },
        { 
            "name": "Namaste Indian Cuisine", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "rating": 4.6,
            "number_of_reviews": 96,
            "cuisine": "Indian",
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

db.commit()
