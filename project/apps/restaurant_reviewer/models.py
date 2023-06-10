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
    Field("number_of_stars", 'integer', default=0),
    Field("number_of_reviews", 'integer', default=0),
    Field("cuisine")
    )

db.define_table(
    'tier_list',
    Field('user_email', default=get_user_email), #user email that added the restaurant
    Field('restaurant_id'),
    fake_migrate=False #from db.restaurant.id
    # Field('created_by', 'reference auth_user',
    #       default=lambda: session.user_id),
)

# star rating db
db.define_table('stars',
                Field('restaurant_id', 'reference restaurant'), # restaurant that is starred
                Field('rating', 'integer', default=0),
                Field('rater', default=get_user_email),
    fake_migrate=False # user doing the rating
                )


if db(db.restaurant).isempty():
    restaurants = [
        { 
            "name": "Hula\'s Island Grill", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 9222,
            "number_of_reviews": 2096,
            "cuisine": "Hawaiian"           
        },
        { 
            "name": "Jack\'s Hamburgers", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 4397,
            "number_of_reviews": 977,
            "cuisine": "American"            
        },
        { 
            "name": "Taqueria Los Pericos", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 9642,
            "number_of_reviews": 2096,
            "cuisine": "Mexican"            
        },
        { 
            "name": "Jack in the Box", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 5843,
            "number_of_reviews": 1623,
            "cuisine": "American"            
        },
        { 
            "name": "Ideal Bar & Grill", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 9268,
            "number_of_reviews": 2317,
            "cuisine": "American"           
        },
        { 
            "name": "Poke House", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 1062,
            "number_of_reviews": 247,
            "cuisine": "Hawaiian Fusion"            
        },
        { 
            "name": "The Poke Bowl", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 671,
            "number_of_reviews": 156,
            "cuisine": "Hawaiian Fusion"            
        },
        { 
            "name": "Sabieng Thai Cuisine", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 1716,
            "number_of_reviews": 399,
            "cuisine": "Thai"           
        },
        { 
            "name": "Real Thai Kitchen", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 1300,
            "number_of_reviews": 317,
            "cuisine": "Thai"           
        },
        { 
            "name": "Royal Taj India Cuisine", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 1004,
            "number_of_reviews": 239,
            "cuisine": "Indian"           
        },
        { 
            "name": "L & L Hawaiian Barbeque", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 2444,
            "number_of_reviews": 596,
            "cuisine": "Hawaiian"            
        },
        { 
            "name": "Namaste Indian Cuisine", 
            "city": "Santa Cruz",
            "zipCode": 95060,
            "number_of_stars": 442,
            "number_of_reviews": 96,
            "cuisine": "Indian"           
        },
        { 
            "name": "Louders", 
            "city": "Los Angeles",
            "zipCode": 90020,
            "number_of_stars": 673,
            "number_of_reviews": 153,
            "cuisine": "Korean"           
        },
        { 
            "name": "The Public Izakaya", 
            "city": "San Francisco",
            "zipCode": 94109,
            "number_of_stars": 409,
            "number_of_reviews": 93,
            "cuisine": "Japanese"           
        },
        { 
            "name": "Tokyo Fried Chicken", 
            "city": "Los Angeles",
            "zipCode": 91754,
            "number_of_stars": 2295,
            "number_of_reviews": 499,
            "cuisine": "Japanese"           
        },
        { 
            "name": "Jollibee", 
            "city": "San Jose",
            "zipCode": 95122,
            "number_of_stars": 3517,
            "number_of_reviews": 818,
            "cuisine": "Filipino"           
        },
        { 
            "name": "Tasty Pot", 
            "city": "San Jose",
            "zipCode": 95129,
            "number_of_stars": 1862,
            "number_of_reviews": 433,
            "cuisine": "Chinese"           
        }
    ]

    for restaurant in restaurants:
        db.restaurant.insert(name=restaurant['name'],
                            city=restaurant['city'],
                            zipCode=restaurant['zipCode'],
                            number_of_stars=restaurant['number_of_stars'],
                            number_of_reviews=restaurant['number_of_reviews'],
                            cuisine=restaurant['cuisine'])

db.commit()
