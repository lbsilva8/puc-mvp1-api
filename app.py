# aplicação para controle de séries que quero assistir

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote

from model import Session, Serie
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
serie_tag = Tag(name="Serie", description="Adição, visualização e remoção de series à base")

@app.get('/', tags=[home_tag])
def homepage():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/serie', tags=[serie_tag],
        responses={"200": SerieViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_serie(form: SerieSchema):
    """Adiciona uma nova série à base de dados
    
    Retorna uma representação dos itens.
    """
    serie = Serie(
        nome = form.nome,
        status = form.status,
        temporada = form.temporada,
        aplicativo = form.aplicativo
    )
    logger.debug(f"Adicionando série de nome: '{serie.nome}'")

    try:
        session = Session()
        session.add(serie)
        session.commit()
        logger.debug(f"Adicionando série de nome: '{serie.nome}'")
        return apresenta_serie(serie), 200

    except IntegrityError as e:
        error_msg = "Serie de mesmo nome já salva na base."
        logger.warning(f"Erro ao adicionar série: '{serie.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg =  "Não foi possivel adicionar novo item."
        logger.warning(f"Erro ao adicionar série: '{serie.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/series', tags=[serie_tag],
         responses={"200": ListagemSeriesSchema, "404": ErrorSchema})
def get_series():
    """ Faz a busca de todas as séries cadastradas
    
    Retorna uma representação da listagem de séries.
    """
    
    logger.debug(f"Coletando series")
    session = Session()
    series = session.query(Serie).all()

    if not series:
        return {"series": []}, 200
    else:
        logger.debug(f"%d series econtradas" % len(series))
        print(series)
        return apresenta_series(series), 200


@app.get('/serie', tags=[serie_tag],
         responses={"200": SerieViewSchema, "404": ErrorSchema})
def get_serie(query: SerieBuscaIdSchema):
    """ Faz a busca da série a partir de um id
    
    Retorna uma representação da série.
    """
    
    serie_id = query.id
    logger.debug(f"Coletando dados sobre serie #{serie_id}")
    session = Session()
    serie = session.query(Serie).filter(Serie.id == serie_id).first()

    if not serie:
        error_msg = "Serie não encontrada na base."
        logger.warning(f"Erro ao buscar serie '{serie_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    else:
        logger.debug(f"Serie econtrada: '{serie_id}'")
        return apresenta_serie(serie), 200
    

@app.delete('/serie', tags=[serie_tag],
            responses={"200": SerieDelSchema, "404": ErrorSchema})
def del_serie(query: SerieBuscaNomeSchema):
    """Deleta uma série a partir do nome
    
    Retorna uma mensagem de confirmação da remoção.
    """

    serie_nome = unquote(unquote(query.nome))
    print(serie_nome)
    logger.debug(f"Deletando dados sobre serie #{serie_nome}")

    session = Session()
    count = session.query(Serie).filter(Serie.nome == serie_nome).delete()
    session.commit()
    
    if count:
        logger.debug(f"Deletado serie #{serie_nome}")
        return {"mesage": "Série removida da base", "nome": serie_nome}
        

    else:
        error_msg = "Serie não encontrada na base."
        logger.warning(f"Erro ao deletar serie #'{serie_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    