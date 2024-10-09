import unittest
from app import create_app, db
from app.models import Product
from app.services import ProductService

product_service = ProductService()

class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()        

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_product(self):
        # Crear un producto de ejemplo en la base de datos
        product = Product(name="Producto de prueba", price=100.0, activated=True)
        product_service.save(product)
        id = product.id

        # Realizar la solicitud GET para obtener el producto por ID
        response = self.client.get(f'/api/v1/get_product/{id}')
        self.assertEqual(response.status_code, 200)

        # Verificar el contenido de la respuesta JSON
        response_data = response.get_json()
        self.assertIn("id", response_data[0])
        self.assertEqual(response_data[0]["id"], id)
        self.assertEqual(response_data[0]["name"], "Producto de prueba")
        self.assertEqual(response_data[0]["price"], 100.0)
        self.assertTrue(response_data[0]["activated"])

    def test_create_product(self):
        product_data = {
            "name": "Nuevo Producto4",
            "price": 150.0,
            "activated": True
        }
        response = self.client.post('/api/v1/create_product', json=product_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Producto Creado Correctamente")

        product = product_service.find_by_name("Nuevo Producto4")
        self.assertIsNotNone(product)
        self.assertEqual(product.price, 150.0)
        self.assertTrue(product.activated)

    def test_check_price(self):
        product = Product(name="Producto5", price=100.0, activated=True)
        product_service.save(product)
        id = product.id

        response = self.client.get(f'/api/v1/product/check_price/{id}')
        
        self.assertEqual(response.status_code, 200)
        
        response_data = response.get_json()
        self.assertIn('price', response_data)
        self.assertEqual(response_data['price'], product.price)

    def test_delete_product(self):
        product = Product(name="Producto6", price=100.0, activated=True)
        product_service.save(product)
        id = product.id
        response = self.client.delete(f'/api/v1/delete_product/{product.id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Producto eliminado', response.data)

        deleted_product = product_service.find(product.id)
        self.assertIsNone(deleted_product)


if __name__ == "__main__":
    unittest.main()