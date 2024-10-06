from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Product(db.Model):
    __tablename__ = "products"
    
    # Definición de los atributos del modelo
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(255), nullable=False)
    precio: float = db.Column(db.Float, nullable=False)
    activado: bool = db.Column(db.Boolean, default=True, nullable=False)