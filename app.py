from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__, static_folder='static')
CORS(app)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/roni"
mongo = PyMongo(app)

# Route to add a new product
@app.route('/product', methods=['POST'])
def add_product():
    products = mongo.db.products
    name = request.json['name']
    price = request.json['price']

    product_id = products.insert_one({'name': name, 'price': price}).inserted_id
    new_product = products.find_one({'_id': product_id})

    return jsonify({'_id': str(ObjectId(new_product['_id'])), 'name': new_product['name'], 'price': new_product['price']})

# Route to list all products
@app.route('/product', methods=['GET'])
def get_products():
    products = mongo.db.products
    result = []
    for field in products.find():
        result.append({'_id': str(field['_id']), 'name': field['name'], 'price': field['price']})
    return jsonify(result)

# Route to get a single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    products = mongo.db.products
    product = products.find_one({'_id': ObjectId(id)})
    return jsonify({'_id': str(product['_id']), 'name': product['name'], 'price': product['price']})

# Route to delete a product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    products = mongo.db.products
    products.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Product deleted'})

# Route to update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    products = mongo.db.products
    products.update_one({'_id': ObjectId(id)}, {"$set": request.json})
    product = products.find_one({'_id': ObjectId(id)})
    return jsonify({'_id': str(product['_id']), 'name': product['name'], 'price': product['price']})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
