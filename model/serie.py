from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from typing import Union

from  model import Base

class Serie(Base):
    __tablename__ = 'serie'

    id = Column("pk_serie", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    status = Column(String(50))
    temporada = Column(Integer)
    aplicativo = Column(String(50))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, status: str, temporada: Integer, aplicativo: str,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria uma nova serie na lista

        Arguments:
        nome: Nome da serie que será adicionada
        status: O status da serie no momento
        temporada: Qual temporada está assistindo
        aplicativo: Qual app está usando para assistir
        data_insercao: Data de inserção da serie à base
        """
        self.nome = nome
        self.status = status
        self.temporada = temporada
        self.aplicativo = aplicativo

        if data_insercao:
            self.data_insercao = data_insercao