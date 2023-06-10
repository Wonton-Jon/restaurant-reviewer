"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import datetime
import random

from py4web.utils.form import Form, FormStyleBulma
from py4web import action, request, abort, redirect, URL, Field
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash, Field
from py4web.utils.url_signer import URLSigner
from .models import get_username, get_user_email

from pydal.validators import (
    IS_MATCH,
    IS_NOT_EMPTY,
)

url_signer = URLSigner(session)
ne = IS_NOT_EMPTY()

# Some constants.
MAX_RETURNED_RESTAURANTS = 20 # Our searches do not return more than 20 users.
MAX_RESULTS = 20 # Maximum number of returned meows. 

def getRating(restaurant):
    if restaurant['number_of_reviews'] != 0.0:
        return float(restaurant['number_of_stars']) / restaurant['number_of_reviews']
    else:
        return 0.0

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        get_current_user_url = URL('get_current_user', signer=url_signer),
        filter_restaurants_url = URL('filter_restaurants', signer=url_signer),
        get_restaurants_url = URL('get_restaurants', signer=url_signer),
        # COMPLETE: return here any signed URLs you need.
        follow_url=URL('set_follow', signer=url_signer),
        set_stars_url=URL('set_stars', signer=url_signer)
    )

#Get the current user
@action("get_current_user", method="GET")
@action.uses(db, auth.user)
def get_current_user():
    rows = db(db.auth_user.username == get_username()).select()
    return dict(rows=rows)

@action("filter_users", method="GET")
@action.uses(db, auth.user)
def filter_users():
    text = request.GET.get("text", "")
    rows = db(db.auth_user.username.contains(text)).select()
    return dict(rows=rows)

#USED FOR PROJECT
@action("get_restaurants")
@action.uses(db)
def get_restaurants():
    #Get the list of ids of restaurants
    restaurants = db(db.restaurant).select().as_list()

    for restaurant in restaurants:
        restaurant['rating'] = round(getRating(restaurant), 1)
    
    restaurants = sorted(restaurants, key=lambda x: x['rating'], reverse=True)

    current_user = get_current_user()
    current_user['email'] = get_user_email()
    
    #Get the restaurants that the user is following
    for restaurant in restaurants:
        restaurant['isFollowed'] = db((db.tier_list.user_email == current_user['email']) & 
                                      (db.tier_list.restaurant_id == restaurant['id'])).count() >= 1

    return dict(restaurants=restaurants)


#Filter through all restaurants to get ones that contain the value text
@action("filter_restaurants", method="GET")
@action.uses(db)
def filter_restaurants():
    text = request.GET.get("text", "")
    rows = db(db.restaurant.name.contains(text)).select(orderby=db.restaurant.name)

    return dict(rows=rows)

#Add restaurant to db
#zipCode must be empty or correct formatted
@action('add', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add.html')
def add_restaurant():
    form = Form([Field('name', required=True, requires=ne), 
                 Field('city'),
                 Field('zipCode', requires=[
                            IS_MATCH(r"^$|(^\d{5}$)|(^\d{9}$)|(^\d{5}-\d{4}$)"),
                        ]),
                 Field('cuisine')
                ],
                csrf_session=session, formstyle=FormStyleBulma)

    #If the form has a nonempty name
    if form.accepted and form.vars["name"]:
        db.restaurant.insert(
            name=form.vars["name"], 
            city=form.vars["city"],
            zipCode=form.vars["zipCode"],
            cuisine=form.vars["cuisine"])
        
        redirect(URL('index'))

    return dict(form=form)

@action("set_follow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def set_follow():
    #Get the follow status and the restaurant ID that was added/removed from the list
    is_followed = request.json.get('is_followed')
    restaurant_id = request.json.get('restaurant_id')

    #If the restaurant is added, then insert to tier list
    #Otherwise remove from the tier list
    if is_followed:
        db.tier_list.insert(
            user_email=get_user_email(),
            restaurant_id=restaurant_id
        )
    else:
        db((db.tier_list.user_email == get_user_email()) & (db.tier_list.restaurant_id == restaurant_id)).delete()


@action("set_stars", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def set_stars():

    
    # axios.post(set_stars_url, {restaurant_id: restaurant.id, rating: num_stars});
    restaurant_id = request.json.get('restaurant_id')
    rating = request.json.get('rating')

    # db.stars.insert(restaurant_id=restaurant_id, rating=rating, rater=get_user_email() )

    # db((db.stars.rater == get_user_email()) & (db.stars.restaurant_id == restaurant_id)).delete()
    current_restaurant = db(db.restaurant.id==restaurant_id).select().as_list()[0]
    old_num_stars = current_restaurant['number_of_stars']
    old_num_reviews = current_restaurant['number_of_reviews']

    # if rating exists, delete and make new, else insert new rating into db
    item = db((db.stars.restaurant_id == restaurant_id) & (db.stars.rater == get_user_email())).select().as_list()

    if len(item) != 0:
        print('\n\n\ninside of the true part\n\n\n')

        old_stars_row = db((db.stars.rater == get_user_email()) & (db.stars.restaurant_id == restaurant_id)).select().as_list()
        old_rating = old_stars_row[0]['rating']

        new_num_stars = old_num_stars - old_rating + rating

        db((db.stars.rater == get_user_email()) & (db.stars.restaurant_id == restaurant_id)).delete()
        db.stars.insert(restaurant_id=restaurant_id, rating=rating, rater=get_user_email())

        #update the numver of stars in restaurants
        db.restaurant.update_or_insert(db.restaurant.id == restaurant_id,
                                       number_of_stars=new_num_stars)

        # new_star_count = db.restaurant.number_of_stars + rating - old_rating

        # if (db.stars.restaurant_id == restaurant_id):
        #     db.restaurant.insert(number_of_stars=new_star_count)
        
        
    else:
        print('\n\n\ninside of the eASDFKJASLDFASDFASDF ue part\n\n\n')

        new_num_stars = old_num_stars + rating
        new_num_reviews = old_num_reviews + 1

        db.stars.insert(restaurant_id=restaurant_id, rating=rating, rater=get_user_email())

        #update the numver of stars in restaurants
        db.restaurant.update_or_insert(db.restaurant.id == restaurant_id,
                                       number_of_stars=new_num_stars,
                                       number_of_reviews=new_num_reviews)
    

    #Get the follow status and the restaurant ID that was added/removed from the list
    # stars_id = request.json.get('stars_id')
    # restaurant_id = request.json.get('restaurant_id')

    # #If the restaurant is added, then insert to tier list
    # #Otherwise remove from the tier list
    # if stars_id is None:
    #     db.stars.insert(
    #         restaurant_id=restaurant_id,
    #         # rating=num_stars,
    #         rater=get_user_email()
    #     )
    # else:
    #     db((db.stars.rater == get_user_email()) & (db.stars.restaurant_id == restaurant_id)).delete()
    
    # if db.stars.u_rating is None:
    #     db.stars.insert(u_rating=0)





# # star rating modules
# @action('get_rating')
# @action.uses(url_signer.verify(), db, auth.user)
# def get_rating():
#     """Returns the rating for a user and an restaurant."""
#     restaurant_id = request.params.get('restaurant_id')
#     row = db((db.stars.restaurant_id == restaurant_id) &
#              (db.stars.rater == get_user_email())).select().first()
#     rating = row.rating if row is not None else 0
#     return dict(rating=rating)

# @action('set_rating', method='POST')
# @action.uses(url_signer.verify(), db, auth.user)
# def set_rating():
#     """Sets the rating for an restaurant."""
#     restaurant_id = request.json.get('restaurant_id')
#     rating = request.json.get('rating')
#     assert restaurant_id is not None and rating is not None
#     db.stars.update_or_insert(
#         ((db.stars.restaurant_id == restaurant_id) & (db.stars.rater == get_user_email())),
#         restaurant_id=restaurant_id,
#         rater=get_user_email(),
#         rating=rating
#     )
#     return "ok" # Just to have some confirmation in the Network tab.