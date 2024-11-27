from slugify import slugify

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

class ProductAdd(BaseModel):
    title: str
    description: str | None = None
    quantity: int
    price: int
    category_id: int
    slug: str
    
class Product(ProductAdd):
    id: int
        