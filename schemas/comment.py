from pydantic import BaseModel


class CommentSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    product_id: int = 1
    text: str = "Revisar o Produto Antes de Adicionar!"
