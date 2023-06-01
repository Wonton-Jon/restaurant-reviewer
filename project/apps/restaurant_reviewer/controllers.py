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
from .models import get_username

from pydal.validators import (
    CRYPT,
    IS_EMAIL,
    IS_EQUAL_TO,
    IS_MATCH,
    IS_NOT_EMPTY,
    IS_NOT_IN_DB,
    IS_STRONG,
)

url_signer = URLSigner(session)
ne = IS_NOT_EMPTY()

# Some constants.
MAX_RETURNED_RESTAURANTS = 20 # Our searches do not return more than 20 users.
MAX_RESULTS = 20 # Maximum number of returned meows. 

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        get_current_user_url = URL('get_current_user', signer=url_signer),
        filter_restaurants_url = URL('filter_restaurants', signer=url_signer),
        get_restaurants_url = URL('get_restaurants', signer=url_signer),
        # COMPLETE: return here any signed URLs you need.
        follow_url=URL('set_follow', signer=url_signer),
    )


@action("set_follow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def set_follow():
    #Get the username 
    username = request.json.get("username")
    followed_user = db(db.auth_user.username == username).select().first()

    #if the user exists then update the following
    if followed_user:
        followed = db((db.follow.follower == auth.current_user.get("id")) & (db.follow.followed == followed_user.id)).select().first()
        
        #Delete the user if they are followed, otherwise add them
        if followed:
            db(db.follow.id == followed.id).delete()
        else:
            db.follow.insert(follower=auth.current_user.get("id"), followed=followed_user.id)
        return dict(success=True)
    else:
        return dict(success=False)

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
    restaurants = db(db.restaurant).select(orderby=~db.restaurant.rating).as_list()

    #Get the restaurants that the user is following


    return dict(restaurants=restaurants)



@action("filter_restaurants", method="GET")
@action.uses(db)
def filter_restaurants():
    text = request.GET.get("text", "")
    rows = db(db.restaurant.name.contains(text)).select(orderby=db.restaurant.name)
    print('in filter_restaurants\n\n\n')
    print(rows)
    print('\n\n\n')
    return dict(rows=rows)

@action('add', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add.html')
def add_restaurant():
    form = Form([Field('name', required=True, requires=ne), 
                 Field('city'),
                 Field('zipCode', requires=[
                            IS_MATCH(r"^$|(^\d{5}$)|(^\d{9}$)|(^\d{5}-\d{4}$)"),
                        ]),
                 Field('cuisine'),
                 Field('is_fastfood', default=False)
                ],
                csrf_session=session, formstyle=FormStyleBulma)

    if form.accepted and form.vars["name"]:
        db.restaurant.insert(
            name=form.vars["name"], 
            city=form.vars["city"],
            zipCode=form.vars["zipCode"],
            rating=0.0,
            number_of_reviews=0,
            cuisine=form.vars["cuisine"],
            is_fastfood=form.vars["is_fastfood"])
        
        redirect(URL('index'))

    return dict(form=form)