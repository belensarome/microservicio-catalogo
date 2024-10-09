from flask import Blueprint, request, jsonify
from app.services import ProductService
# from app.models.stock import Stock
# from app.repositories.stock_repo import StockRepo
# from app.services.ms_stock import StockService

product = Blueprint("product", __name__)
product_service = ProductService()

@product.route("/", methods=["GET"])
def home():
    return "ya algo funciona", 200

@product.route("/get_product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = product_service.get_product_by_id(product_id)
    data = [{"id" : product.id, "nombre" : product.nombre, "precio" : product.precio, "activado" : product.activado}]
    return jsonify(data), 200
