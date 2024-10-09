from typing import List
from app.models import Product
from app import db

class ProductRepository:
    def save(self, product: Product) -> Product:
        """Guarda un nuevo producto en la base de datos."""
        db.session.add(product)
        db.session.commit()
        return product

    def update(self, product: Product, id: int) -> Product:
        """Actualiza un producto existente en la base de datos."""
        entity = self.find(id)
        if entity is None:
            return None
        entity.nombre = product.nombre
        entity.precio = product.precio
        entity.activado = product.activado

        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, product: Product) -> None:
        """Elimina un producto de la base de datos."""
        db.session.delete(product)
        db.session.commit()

    def all(self) -> List[Product]:
        """Devuelve una lista de todos los productos en la base de datos."""
        products = db.session.query(Product).all()
        return products

    def get_product_id(self, id: int) -> Product:
        """Busca un producto por su ID y que esté activo (activo = true)."""
        if id is None or id == 0:
            return None
        try:
            return db.session.query(Product).filter(Product.id == id, Product.activado == True).one()
        except:
            return None
    
    def find(self, id: int) -> Product:
        """Busca un producto por su ID."""
        if id is None or id == 0:
            return None
        try:
            return db.session.query(Product).filter(Product.id == id).one()
        except:
            return None

    def find_by_name(self, nombre: str) -> Product:
        """Busca un producto por su nombre."""
        return db.session.query(Product).filter(Product.nombre == nombre).one_or_none()

    def find_by_price(self, precio: float) -> List[Product]:
        """Busca productos por su precio."""
        return db.session.query(Product).filter(Product.precio == precio).all()

