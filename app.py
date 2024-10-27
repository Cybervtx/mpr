# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Modelagem
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

@app.route('/api/products/add', methods=['POST'])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data['name'],price=data['price'],description=data.get("description",""))
        try:
            db.session.add(product)
            db.session.commit()
            return jsonify({"message": "Produto cadastrado com sucesso"}), 201
        except IntegrityError :
            return jsonify({"message": "Produto Já existe"}), 409
    return jsonify({"message": "Invalid product data"}), 400

# Definir uma rota raiz (pagina inicial)
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)