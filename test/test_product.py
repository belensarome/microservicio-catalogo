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
        new_product = Product(name="Producto Test", price=100.0, activated=True)
        product_service.save(new_product)

        # Verifica que el producto se ha guardado correctamente
        product = product_service.find_by_name("Producto Test")
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Producto Test")
        self.assertEqual(product.price, 100.0)
        self.assertTrue(product.activated)

    def test_update_product(self):
        """Verifica que se puede actualizar un producto."""
        new_product = Product(name="Producto Test", price=100.0, activated=True)
        product_service.save(new_product)
        id = new_product.id

        # Actualiza el producto
        #product = product_service.find_by_name("Producto Test")
        new_product.price = 150.0

        product_service.update(new_product, id)

        # Verifica que el price ha sido actualizado
        updated_product = product_service.find_by_name("Producto Test")
        self.assertEqual(updated_product.price, 150.0)

    def test_delete_product(self):
        """Verifica que se puede eliminar un producto."""
        new_product = Product(name="Producto Test", price=100.0, activated=True)
        product_service.save(new_product)

        # Elimina el producto
        product = product_service.find_by_name("Producto Test")
        db.session.delete(product)
        db.session.commit()

        # Verifica que el producto ha sido eliminado
        deleted_product = product_service.find_by_name("Producto Test")
        self.assertIsNone(deleted_product)

    def test_deactivate_product(self):
        """Verifica que se puede desactivar un producto."""
        new_product = Product(name="Producto Test", price=100.0, activated=True)
        product_service.save(new_product)

        # Desactiva el producto
        product = product_service.find_by_name("Producto Test")
        product.activated = False
        db.session.commit()

        # Verifica que el producto está desactivado
        deactivated_product = product = product_service.find_by_name("Producto Test")
        self.assertFalse(deactivated_product.activated)
    
    def test_check_price(self):
        new_product = Product(name="Producto Test2", price=255.0, activated=True)
        product_service.save(new_product)

        price = product_service.check_price(new_product.id)
        self.assertEqual(price, 255.0)


    def test_check_availability(self):
        new_product = Product(name="Producto Test2", price=100.0, activated=True)
        product_service.save(new_product)

        availability = product_service.check_availability(new_product.id)
        self.assertTrue(availability)

        new_product.activated = False
        #product_service.save(product)
        availability = product_service.check_availability(new_product.id)
        self.assertFalse(availability)

    def test_check_availability_name(self):
        new_product = Product(name="Producto Test2", price=100.0, activated=True)
        product_service.save(new_product)

        product = product_service.find_by_name("Producto Test2")
        availability = product_service.check_availability_name("Producto Test2")
        self.assertTrue(availability)

        product.activated = False
        #product_service.save(product)
        availability = product_service.check_availability_name("Producto Test2")
        self.assertFalse(availability)

    def test_get_product_by_id_exists_and_active(self):
        product = Product(id=1, name="Producto de prueba", price=100.0, activated=True)
        product_service.save(product)
        result = product_service.get_product_by_id(1)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
        self.assertTrue(result.activated)

    def test_get_product_by_id_not_active(self):
        inactive_product = Product(id=2, name="Producto inactivo", price=50.0, activated=False)
        product_service.save(inactive_product)
        result = product_service.get_product_by_id(2)

        self.assertIsNone(result)

    