#!/usr/bin/env python2.7


# Imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import desc, literal
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from database_setup import Base, Category, Item, User, engine
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# Flask instance
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"


# Create session and connect to DB
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/logout')
def aLogout():
    if login_session['provider'] == 'facebook':
        fbdisconnect()
        login_session.clear()
        return redirect(url_for('showHome'))    


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("access token received %s " % access_token)

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'], 'success')
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    return "you have been logged out"




# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Flask Routes
# all catalog - JSON
@app.route('/api/catalog/')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.Serialize for c in categories])


# A specific category data with items- JSON
@app.route('/api/catalog/categories/<int:category_id>/')
def catalogSpecificCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.Serialize)

# all categories data without items - JSON
@app.route('/api/categories/')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.shortSerialize for c in categories])

# a specific category data without items - JSON
@app.route('/api/categories/<int:category_id>/')
def specificCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.shortSerialize)

# a specific category items data - JSON
@app.route('/api/categories/<int:category_id>/items/')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(cat_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])

# a specific item data - JSOM
@app.route('/api/categories/<int:category_id>/items/<int:item_id>/')
def ItemsJSON(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


# Root/Home
@app.route('/')
def showHome():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc())[0:12]
    return render_template('showHome.html', categories=categories, items=items)


# Catalog Category web page
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showCatalogCategory(category_id):
    categories = session.query(Category).all()
    try:
        category = session.query(Category).filter_by(id=category_id).one()
    except NoResultFound:
        flash("Error: The category with id '%s' does not exist." %
              category_id, "error")
        return redirect(url_for('showHome'))

    items = session.query(Item).filter_by(cat_id=category_id).all()
    return render_template('showCatalogCategory.html', categories=categories,
                           sCategory=category, items=items, login_session=login_session)


# create a new Catalog Category
@app.route('/admin/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=1)
        session.add(newCategory)
        session.commit()
        flash("New Category Created!", "success")
        return redirect(url_for('newCategory'))
    else:
        return render_template('newCategory.html', login_session=login_session)


# Edit a Catalog Category
@app.route('/admin/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    try:
        editedCategory = session.query(
            Category).filter_by(id=category_id).one()
    except NoResultFound:
        flash("Error: The category with id '%s' does not exist." %
              category_id, "error")
        return redirect(url_for('showHome'))
    if request.method == 'POST':
        session.add(editedCategory)
        session.commit()
        flash("Category updated!", "success")
        return redirect(url_for('editCategory', category_id=editedCategory.id))
    else:
        return render_template('editCategory.html', category=editedCategory, login_session=login_session)


# Delete a Category
@app.route('/admin/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    try:
        categoryToDelete = session.query(
            Category).filter_by(id=category_id).one()
    except NoResultFound:
        flash("Error: The Item with id '%s' does not exist." %
              category_id, "error")
        return redirect(url_for('showHome'))
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash("Category deleted!", "success")
        return redirect(url_for('showHome'))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete, login_session=login_session)


# Catalog item web page
@app.route('/categories/<int:category_id>/items/<int:item_id>/')
def showCatalogItem(category_id, item_id):
    categories = session.query(Category).all()
    try:
        item = session.query(Item).filter_by(id=item_id).one()
        category = session.query(Category).filter_by(id=item.cat_id).one()
    except NoResultFound:
        flash("Error: The Item with id '%s' does not exist." % item_id, "error")
        return redirect(url_for('showHome'))
    return render_template('showCatalogItem.html', category=category,
                           item=item, categories=categories, login_session=login_session)


# Create Catalog Item
@app.route('/items/new/', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newItem(category_id=0):
    categories = session.query(Category).all()
    if 'username' not in login_session:
        flash("Please, login to your account to proceed!", "error")
        if category_id == 0 :
            return redirect(url_for('showHome'))
        else:
            return redirect(url_for('showCatalogCategory', category_id=category_id))
    if request.method == 'POST':
        newItem = Item(title=request.form['title'], description=request.form['description'],
                       cat_id=request.form['categoryId'], user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("Item created!", "success")
        return redirect(url_for('showCatalogItem', category_id=newItem.cat_id, item_id=newItem.id))
    else:
        return render_template('newItem.html', categories=categories, category_id=category_id, login_session=login_session)


# Edit a Catalog Item
@app.route('/categories/<int:category_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    categories = session.query(Category).all()
    try:
        editedItem = session.query(Item).filter_by(id=item_id).one()
    except NoResultFound:
        flash("Error: The Item with id '%s' does not exist." % item_id, "error")
        return redirect(url_for('showCatalogCategory', category_id=category_id))
    if 'username' not in login_session:
        flash("Please, login to your account to proceed!", "error")
        return redirect(url_for('showCatalogItem', category_id=editedItem.cat_id, item_id=item_id))
    if editedItem.user_id != login_session['user_id']:
        flash("Only the Owner can edit this Item", "error")
        return redirect(url_for('showCatalogItem', category_id=editedItem.cat_id, item_id=item_id))
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['categoryId']:
            editedItem.cat_id = request.form['categoryId']

        session.add(editedItem)
        session.commit()
        flash("Item updated!", "success")
        return redirect(url_for('showCatalogItem', category_id=editedItem.cat_id, item_id=editedItem.id))
    else:
        if editedItem.cat_id != category_id:
            return redirect(url_for('editItem', category_id=editedItem.cat_id, item_id=editedItem.id))
        else:
            return render_template('editItem.html', item=editedItem, categories=categories, login_session=login_session)


# Delete a Category item
@app.route('/categories/<int:category_id>/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    try:
        itemToDelete = session.query(Item).filter_by(id=item_id).one()
    except NoResultFound:
        flash("Error: The Item with id '%s' does not exist." % item_id, "error")
        return redirect(url_for('showCatalogCategory', category_id=category_id))
    if 'username' not in login_session:
        flash("Please, login to your account to proceed!", "error")
        return redirect(url_for('showCatalogItem', category_id=itemToDelete.cat_id, item_id=item_id))
    if itemToDelete.user_id != login_session['user_id']:
        flash("Only the Owner can delete this Item", "error")
        return redirect(url_for('showCatalogItem', category_id=itemToDelete.cat_id, item_id=item_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted!", "success")
        return redirect(url_for('showCatalogCategory', category_id=category_id))
    else:
        if itemToDelete.cat_id != category_id:
            return redirect(url_for('deleteItem', category_id=itemToDelete.cat_id, item_id=itemToDelete.id))
        else:
            return render_template('deleteItem.html', item=itemToDelete, login_session=login_session)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
