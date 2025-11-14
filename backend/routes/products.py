from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from db import SessionLocal
from models.product import Product

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.get("/")
def list_products():
    session = SessionLocal()
    try:
        products = session.query(Product).all()
        return jsonify([p.to_dict() for p in products])
    finally:
        session.close()

@products_bp.post("/")
def create_product():
    data = request.get_json() or {}
    required_fields = ["name", "sku", "price", "stock_quantity"]

    # Basic validation: make sure required fields exist
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    session = SessionLocal()
    try:
        product = Product(
            name=data["name"],
            sku=data["sku"],
            price=float(data["price"]),
            stock_quantity=int(data["stock_quantity"]),
        )
        session.add(product)
        session.commit()
        session.refresh(product)  # refresh from DB so it has its new id
        return jsonify(product.to_dict()), 201

    except IntegrityError:
        session.rollback()
        return jsonify({"error": "SKU must be unique"}), 400

    finally:
        session.close()

@products_bp.put("/<int:product_id>")
def update_product(product_id):
    data = request.get_json() or {}

    session = SessionLocal()
    try:
        # Find the existing product by ID
        product = session.get(Product, product_id)
        if product is None:
            return jsonify({"error": "Product not found"}), 404

        # Update only the fields that were sent
        if "name" in data:
            product.name = data["name"]
        if "sku" in data:
            product.sku = data["sku"]
        if "price" in data:
            product.price = float(data["price"])
        if "stock_quantity" in data:
            product.stock_quantity = int(data["stock_quantity"])

        session.commit()
        session.refresh(product)

        return jsonify(product.to_dict())

    except IntegrityError:
        session.rollback()
        return jsonify({"error": "SKU must be unique"}), 400

    finally:
        session.close()

@products_bp.delete("/<int:product_id>")
def delete_product(product_id):
    session = SessionLocal()
    try:
        product = session.get(Product, product_id)
        if product is None:
            return jsonify({"error": "Product not found"}), 404

        session.delete(product)
        session.commit()

        return jsonify({"message": "Product deleted"})

    finally:
        session.close()
