#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "baked_goods": [],
            "created_at": "2023-11-03 16:11:18",
            "id": bakery.id,
            "name": bakery.name,
            "updated_at": bakery.updated_at
        }
        bakeries.append(bakery_dict)
    response = make_response(
        jsonify(bakeries),
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first().to_dict()
    response = make_response(
        jsonify(bakery),
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = [baked_good.to_dict() for baked_good in BakedGood.query.order_by(BakedGood.price.desc()).all()]
    response = make_response(
        jsonify(baked_goods),
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first().to_dict()
    response = make_response(
        jsonify(baked_good),
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
