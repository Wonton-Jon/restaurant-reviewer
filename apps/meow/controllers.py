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

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_username

url_signer = URLSigner(session)

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
        get_users_url = URL('get_users', signer=url_signer),
        follow_url=URL('set_follow', signer=url_signer),
    )

@action("get_users")
@action.uses(db, auth.user)
def get_users():
    #Get the list of ids of users followed
    users_followed = db(db.follow.follower == auth.current_user.get("id")).select(db.follow.followed).as_list()
    ids_followed = []
    for user in users_followed:
        ids_followed.append(user["followed"])

    #Create a dictionary with format (k,v) => (username : Boolean) 
    #True if followed false otherwise
    following = db(db.auth_user.id.belongs(ids_followed)).select(db.auth_user.username).as_list()
    for user in following:
        user['isFollowing'] = True
    
    #Get list of unfollowed users
    not_following = db(~db.auth_user.id.belongs(ids_followed)).select(db.auth_user.username).as_list()
    for user in not_following:
        user['isFollowing'] = False
    return dict(followed=following, unfollowed=not_following)


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