# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)


# Modelando Usuarios
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)


# Modelagem do banco de dados
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


# Definir uma rota raiz (pagina inicial)
@app.route('/')
def home():
    return 'PROJETO MPR'


# Login do usuario
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and data.get("password") == user.password:
        return jsonify({"message": "Logado"})
    return jsonify({"message": "Nao autorizado"}), 401


# Adicionando produto ao banco de dados
@app.route('/api/products/add', methods=['POST'])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(
            name=data['name'], price=data['price'], description=data.get("description", ""))
        try:
            db.session.add(product)
            db.session.commit()
            return jsonify({"message": "Produto cadastrado com sucesso"}), 201
        except IntegrityError:
            return jsonify({"message": "Produto Já existe"}), 409
    return jsonify({"message": "Invalid product data"}), 400


# Excluindo produto do banco de dados
@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produto deletado com sucesso"}), 200
    return jsonify({"message": "Produto nao encontrado"}), 404


# Recuperando detalhes de um produto
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }), 200
    return jsonify({"message": "Produto nao encontrado"}), 404


# Atualizando dados de um produto
@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
def upadte_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"message": "Produto nao encontrado"}), 404

    data = request.json

    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()

    return jsonify({"message": "Produto atualizado"}), 200


# Recuperar todos os produtos
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    list = [{'id': product.id, 'name': product.name, 'price': product.price,
             'description': product.description} for product in products]
    if len(list) == 0:
        return jsonify({"message": "Nao existe produtos cadastrados"}), 404
    return jsonify(list)


if __name__ == '__main__':
    app.run(debug=True)
