from pydantic import BaseModel

class CategoryAdd(BaseModel):
    title: str
    slug: str

class Category(CategoryAdd):
    id: int