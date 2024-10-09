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

        # Crear un producto de ejemplo en la base de datos
        self.product = Product(id=1, nombre="Producto de prueba", precio=100.0, activado=True)
        product_service.save(self.product)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_product(self):
        # Realizar la solicitud GET para obtener el producto por ID
        response = self.client.get('/api/v1/get_product/1')
        self.assertEqual(response.status_code, 200)

        # Verificar el contenido de la respuesta JSON
        response_data = response.get_json()
        self.assertIn("id", response_data[0])
        self.assertEqual(response_data[0]["id"], 1)
        self.assertEqual(response_data[0]["nombre"], "Producto de prueba")
        self.assertEqual(response_data[0]["precio"], 100.0)
        self.assertTrue(response_data[0]["activado"])

if __name__ == "__main__":
    unittest.main()