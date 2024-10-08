import os
import unittest
from flask import current_app
from app import create_app, db
from app.models import Product
from app.services import ProductService

product_service = ProductService()

class ProductTestCase(unittest.TestCase):
    def setUp(self):        
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)
    
    def test_create_product(self):
        """Verifica que se puede crear y guardar un producto en la base de datos."""
        new_product = Product(nombre="Producto Test", precio=100.0, activado=True)
        product_service.save(new_product)

        # Verifica que el producto se ha guardado correctamente
        product = product_service.find_by_name("Producto Test")
        self.assertIsNotNone(product)
        self.assertEqual(product.nombre, "Producto Test")
        self.assertEqual(product.precio, 100.0)
        self.assertTrue(product.activado)

    def test_update_product(self):
        """Verifica que se puede actualizar un producto."""
        new_product = Product(nombre="Producto Test", precio=100.0, activado=True)
        db.session.add(new_product)
        db.session.commit()

        # Actualiza el producto
        product = product_service.find_by_name("Producto Test")
        product.precio = 150.0
        db.session.commit()

        # Verifica que el precio ha sido actualizado
        updated_product = Product.query.filter_by(nombre="Producto Test").first()
        self.assertEqual(updated_product.precio, 150.0)

    def test_delete_product(self):
        """Verifica que se puede eliminar un producto."""
        new_product = Product(nombre="Producto Test", precio=100.0, activado=True)
        db.session.add(new_product)
        db.session.commit()

        # Elimina el producto
        product = product_service.find_by_name("Producto Test")
        db.session.delete(product)
        db.session.commit()

        # Verifica que el producto ha sido eliminado
        deleted_product = Product.query.filter_by(nombre="Producto Test").first()
        self.assertIsNone(deleted_product)

    def test_deactivate_product(self):
        """Verifica que se puede desactivar un producto."""
        new_product = Product(nombre="Producto Test", precio=100.0, activado=True)
        db.session.add(new_product)
        db.session.commit()

        # Desactiva el producto
        product = product_service.find_by_name("Producto Test")
        product.activado = False
        db.session.commit()

        # Verifica que el producto está desactivado
        deactivated_product = product = product_service.find_by_name("Producto Test")
        self.assertFalse(deactivated_product.activado)
