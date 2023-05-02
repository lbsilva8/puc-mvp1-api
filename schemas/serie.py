from pydantic import BaseModel
from typing import Optional, List
from model.serie import Serie


class SerieSchema(BaseModel):
    """Define como uma nova serie deve ser representada ao ser adicionada
    """
    nome: str = "Wandinha"
    status: Optional[str] = "Aguardando"
    temporada: float = 1.0
    aplicativo: str = "Netflix"

class SerieBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da serie.
    """
    nome: str = "Wandinha"

class SerieBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da serie.
    """
    id: int = 1

class ListagemSeriesSchema(BaseModel):
    """Define como uma listagem de series será retornada.
    """
    series:List[SerieSchema]

def apresenta_series(series: List[Serie]):
    """ Retorna uma representação da serie seguindo o schema definido em
        SerieViewSchema.
    """
    result = []
    for serie in series:
        result.append({
            "nome": serie.nome,
            "status": serie.status,
            "temporada": serie.temporada,
            "aplicativo": serie.aplicativo,
        })
    return {"series": result}

class SerieViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    nome: str = "Wandinha"
    status: str = "Aguardando"
    temporada: float = 1.0
    aplicativo: str = "Netflix"

class SerieDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_serie(serie: Serie):
    """ Retorna uma representação da serie seguindo o schema definido em
        SerieViewSchema.
    """
    return{
        "id": serie.id,
        "nome": serie.nome,
        "status": serie.status,
        "temporada": serie.temporada,
        "aplicativo": serie.aplicativo,
    }