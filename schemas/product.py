from pydantic import BaseModel
from typing import Optional, List
from model.product import Product

from schemas import CommentSchema




class ProductQuantitySchema(BaseModel):
    id: int
    quantity: int
   


class ProductSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    id: int 
    title: Optional[str]
    price: Optional[str] 
    quantity: Optional[int]
    category: Optional[str] 
    description: Optional[str]
    image: Optional[str] 
    price: Optional[str] 
        
    

class ProductBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do produto.
    """
    id: str



class ProductslistSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    products:List[ProductSchema]


def apresenta_products(products: List[Product]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProductViewSchema.
    """
    result = []
    for product in products:   
        result.append({
            "id": product.id, # "pk_product" é o nome da coluna no banco
            "title": product.title,
            "price": product.price,
            "quantity": product.quantity, 
            "category": product.category,
            "description": product.description,
            "image": product.image,
                                   
        })

    return {"products": result}


class ProductViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int 
    title: Optional [str] 
    price: Optional [str] 
    quantity: Optional [int]
    category: Optional [str] 
    description: Optional [str] 
    image: Optional [str]   
   

    
class ProductDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: str

def apresenta_product(product: Product):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProductViewSchema.
    """
    return {
        "id": product.id,
        "title": product.title,
        "price": product.price,
        "quantity": product.quantity,
        "category": product.category,
        "description": product.description,
        "image": product.image,
                      
        
    }
