from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config_shop import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)

if __name__ == '__main__':
    app.logger.debug('A value for debugging')
    app.run(debug=True)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    telephone = db.Column(db.String(250), nullable=False)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'))
    product_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_id = db.Column(db.Integer, nullable=True)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))


# class OrdersItems(db.Model):
#     order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))

def fetchCategoriesFromDB():
    return Categories.query.all()

def fetchProductsFromDB(categoryId):
    if categoryId == 0:
        return Products.query.all()
    else:
        return db.session.query(Products).filter_by(category_id = categoryId).all()


# Configure Flask logging
app.logger.setLevel(logging.INFO)  # Set log level to INFO
handler = logging.FileHandler('app.log')  # Log to a file
app.logger.addHandler(handler)

@app.errorhandler(500)
def server_error(error):
    app.logger.exception('An exception occurred during a request.')
    return 'Internal Server Error', 500

@app.route('/logger')
def logger():
    app.logger.info('This is an INFO message')
    app.logger.debug('This is a DEBUG message')
    app.logger.warning('This is a WARNING message')
    app.logger.error('This is an ERROR message')
    app.logger.critical('This is a CRITICAL message')
    return 'Hello, World!'


@app.route('/')
def index():
    categories = fetchCategoriesFromDB()
    products = fetchProductsFromDB(0)
    app.logger.error('the index function is called')
    return render_template('shop.html', categoriesLen=len(categories), categories=categories, productsLen=len(products), products=products)

@app.route('/categories/<id>', methods=['GET'])
def get_product_by_category(id):
    categories = fetchCategoriesFromDB()
    products = fetchProductsFromDB(int(id))
    # products = []

    # for item in allProducts:
    #     print(str(item.category_id) + "product name " +  item.product_name)
    #     if item.category_id == int(id):
    #         products.append(item)

    print(products)
    return render_template('shop.html', categoriesLen=len(categories), categories=categories, productsLen=len(products),
                           products=products)


