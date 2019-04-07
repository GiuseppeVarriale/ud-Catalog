#!/usr/bin/env python3.7

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import desc, literal
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, redirect, url_for, request, flash,\
    jsonify
from database_setup import Base, Category, Item, User, engine

app = Flask(__name__)


# Create session and connect to DB

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
    items = session.query(Item).filter_by(cat_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/api/categories/<int:category_id>/items/<int:item_id>/')
def ItemsJSON(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


# Show root web page with lastest items
@app.route('/')
def showHome():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc())
    return render_template('showHome.html', categories=categories, items=items)

# Show a Catalog Category web page
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showCatalogCategory(category_id):
    categories = session.query(Category).all()
    try:
        category = session.query(Category).filter_by(id=category_id).one()

    except NoResultFound:
        flash("Error: The category with id '%s' does not exist." % category_id, "error")
        return redirect(url_for('showHome'))

    items = session.query(Item).filter_by(cat_id=category_id).all()
    return render_template('showCatalogCategory.html', categories=categories,
                           sCategory=category, items=items)

# Show a Catalog item web page
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
                           item=item, categories=categories)

# create a new Catalog Category
@app.route('/admin/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=1)
        session.add(newCategory)
        session.commit()
        flash("New Category Created!" , "success")
        return redirect(url_for('newCategory'))
    else:
        return render_template('newCategory.html')


# Edit a Catalog Category
@app.route('/admin/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    try:
        editedCategory = session.query(
            Category).filter_by(id=category_id).one()
    except NoResultFound:
        flash("Error: The category with id '%s' does not exist." % category_id, "error")
        return redirect(url_for('showHome'))
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash("Category updated!", "success")
        return redirect(url_for('editCategory', category_id=editedCategory.id))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Create Catalog Item
@app.route('/admin/items/new/', methods=['GET', 'POST'])
@app.route('/admin/categories/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newItem(category_id=0):
    categories = session.query(Category).all()

    if request.method == 'POST':
        newItem = Item(title=request.form['title'], description=request.form['description'], cat_id=request.form['categoryId'], user_id=1)
        session.add(newItem)
        session.commit()
        flash("Item created!", "success")
        return redirect(url_for('newItem', category_id=newItem.cat_id))
    else:
        return render_template('newItem.html', categories=categories, category_id=category_id)



# Edit a Catalog Category
@app.route('/admin/categories/<int:category_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    categories = session.query(Category).all()
    try:
        editedItem = session.query(Item).filter_by(id=item_id).one()
    except NoResultFound:
        flash("Error: The Item with id '%s' does not exist." % item_id, "error")
        return redirect(url_for('showHome'))
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
        return redirect(url_for('editItem', category_id=editedItem.cat_id, item_id=editedItem.id))
    else:
        if editedItem.cat_id != category_id:
            return redirect(url_for('editItem', category_id=editedItem.cat_id, item_id=editedItem.id))
        else:   
            return render_template('editItem.html', item=editedItem, categories=categories)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
