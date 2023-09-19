from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comment


class Product(Base):
    __tablename__ = 'product'

    iddb = Column("pk_product", Integer, primary_key=True)
    id = Column(Integer)
    title = Column(String(4000))  
    price = Column(String(140))
    quantity = Column(Integer)
    category = Column(String(4000))
    description = Column(String(4000))
    image = Column(String(4000))
             

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comments = relationship("Comment")

    def __init__(self, id:int , title:str, price:str, quantity:int, category:str, description:str, image:str ):
                 
        """
        Cria um Produto

        Arguments:
            id: id do produto.
            title: nome do produto.
            price: preço do produto.
            quantity: quantidade do produto.
            category: categoria do produto.
            description: descrição do produto.
            image: imagem do produto.
            
                        
        """
        self.id = id
        self.title = title
        self.price = price
        self.quantity = quantity
        self.category = category
        self.description = description
        self.image = image
       
              
                


