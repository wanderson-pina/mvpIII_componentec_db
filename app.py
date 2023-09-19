from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Product, Comment
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
product_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
comment_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/product', tags=[product_tag],
          responses={"200": ProductViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_product(form: ProductSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    product = Product(
        id=form.id,
        title=form.title,
        price=form.price,
        quantity=form.quantity,
        category=form.category,
        description=form.description,
        image=form.image,  )
        

    logger.debug(f"Adicionando produto de nome: '{product.id}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(product)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{product.id}'")
        return apresenta_product(product), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{product.id}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{product.id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/products', tags=[product_tag],
         responses={"200": ProductslistSchema, "404": ErrorSchema})
def get_products():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    products = session.query(Product).all()

    if not products:
        # se não há produtos cadastrados
        return {"products": []}, 200
    else:
        logger.debug(f"%d products founded" % len(products))
        # retorna a representação de produto
        print(products)
        return apresenta_products(products), 200


@app.get('/product', tags=[product_tag],
         responses={"200": ProductViewSchema, "404": ErrorSchema})
def get_product(query: ProductBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto
    Retorna uma representação do produto e comentário associado.
    """
    product_id = query.id
    logger.debug(f"Coletando dados sobre produto #{product_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{product_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto encontrado: '{product.id}'")
        # retorna a representação de produto
        return apresenta_product(product), 200


@app.post('/product/update_quantity', tags=[product_tag],
          responses={"200": ProductViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_product_quantity(form: ProductQuantitySchema):
    """Atualiza a quantidade de um Produto na base de dados

    Retorna uma representação do produto atualizado.
    """
    product_id = form.id
    new_quantity = form.quantity

    logger.debug(f"Atualizando quantidade do produto #{product_id}")
    try:
        # criando conexão com a base
        session = Session()
        # buscando o produto pelo ID
        product = session.query(Product).filter(Product.id == product_id).first()

        if not product:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            logger.warning(f"Erro ao atualizar quantidade do produto '{product_id}', {error_msg}")
            return {"message": error_msg}, 404

        # Atualize a quantidade do produto
        product.quantity = new_quantity
        session.commit()

        logger.debug(f"Quantidade do produto '{product.id}' atualizada com sucesso")
        return apresenta_product(product), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível atualizar a quantidade do produto :/"
        logger.warning(f"Erro ao atualizar quantidade do produto '{product_id}', {error_msg}")
        return {"message": error_msg}, 400
        

        
@app.delete('/product', tags=[product_tag],
            responses={"200": ProductDelSchema, "404": ErrorSchema})
def del_product(query: ProductBuscaSchema):
    """Deleta um Produto a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    product_id = unquote(unquote(query.id))
    print(product_id)
    logger.debug(f"Deletando dados sobre produto #{product_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Product).filter(Product.id == product_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{product_id}")
        return {"mesage": "Produto removido", "id": product_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{product_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comment', tags=[comment_tag],
          responses={"200": ProductViewSchema, "404": ErrorSchema})
def add_comment(form: CommentSchema):
    """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    product_id  = form.product_id
    logger.debug(f"Adicionando comentários ao produto #{product_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao produto '{product_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    text = form.text
    comment = Comment(text)

    # adicionando o comentário ao produto
    product.add_comment(comment)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{product_id}")

    # retorna a representação de produto
    return apresenta_product(product), 200
