from typing import List
from app.models import Product
from app.repositories import ProductRepository

repository = ProductRepository()

class ProductService:
    """ Clase que se encarga de CRUD de productos """
    
    def save(self, product: Product) -> Product:
        return repository.save(product)

    def update(self, product: Product, id: int) -> Product:
        return repository.update(product, id)

    def delete(self, id: int) -> None:
        product = repository.find(id)
        if product:
            repository.delete(product)

    def all(self) -> List[Product]:
        """ Retorna una lista de todos los productos. """
        return repository.all()
    
    def get_product_by_id(self, id:int):
        return repository.get_product_id(id)

    def check_availability(self, id: int) -> bool:
        return repository.find(id).activado

    def check_availability_name(self, nombre: str) -> bool:
        return repository.find_by_name(nombre).activado
    
    def find(self, id: int) -> Product:
        """ Busca un producto por su ID. """
        return repository.find(id)

    def find_by_name(self, nombre: str) -> Product:
        """ Busca un producto por su nombre. """
        return repository.find_by_name(nombre)

    def find_by_price(self, precio: float) -> List[Product]:
        """ Busca productos por su precio. """
        return repository.find_by_price(precio)