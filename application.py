#!/usr/bin/env python3.7

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, redirect, url_for, request, flash,\
    jsonify
from database_setup import Base, Category, Item, User

app = Flask(__name__)


# DB Session maker
# Create session and connect to DB
engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/api/catalog/')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.Serialize for c in categories])


@app.route('/api/catalog/categories/<int:category_id>/')
def catalogSpecificCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.Serialize)


@app.route('/api/categories/')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.shortSerialize for c in categories])


@app.route('/api/categories/<int:category_id>/')
def specificCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.shortSerialize)


@app.route('/api/categories/<int:category_id>/items/')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        cat_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/api/categories/<int:category_id>/items/<int:item_id>/')
def ItemsJSON(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(
        id=item_id).one()
    return jsonify(Item=item.serialize)


# Show root web page
@app.route('/')
def showHome():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('index.html', categories=categories, items=items)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
