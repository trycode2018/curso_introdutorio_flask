from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Criando o modelo produto
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text,nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description
        }

@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"Product added successfuly"})
    return jsonify({"message":"Invalid product data"}), 400


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted successfuly"})
    return jsonify({"message":"Product not found"}), 404

@app.route('/api/products/<int:product_id>')
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        data = product.to_dict()
        return jsonify({
            "message":"Product found successfuly",
            "data":data
            })
    return jsonify({"message":"Product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message":"Product not found"}), 404
    data = request.json
    
    #passando os valores novos 
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.description = data.get('description',product.description)
    
    db.session.commit()
    return jsonify({"message":"Product updated successfuly"})

@app.route('/api/products', methods=["GET"])
def get_products():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    products = Product.query.paginate(page=page,per_page=per_page)

    product_list = []
    for product in products.items:
        product_list.append(product.to_dict())

    return jsonify({
        "data":product_list,
        "page":page,
        "per_page":products.pages,
        "total_items":products.total
    })

if __name__ == "__main__":
    app.run(debug=True)

    