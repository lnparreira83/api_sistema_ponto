from datetime import datetime

from flask_restful.fields import DateTime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///tempo.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class ModeloColaborador(Base):
    __tablename__ = 'colaborador'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(12), nullable=False)
    email = Column(String(255), nullable=True)
    celular = Column(Integer(), nullable=False)
    empresa = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    endereco = Column(String(150), nullable=False)
    cep = Column(String(20), nullable=False)
    ativo = Column(String(3), default='SIM', nullable=False)
    created_at = datetime.utcnow()
    last_modified_at = datetime.utcnow()
    pontos = relationship("Ponto")

    def __repr__(self):
        return '<nome do colaborador {}>'.format(self.valor_presente_liquido)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class ModeloPonto(Base):
    __tablename__ = "ponto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_de_ponto = Column(String(10), nullable=False)
    created_at = datetime.utcnow()
    last_modified_at = datetime.utcnow()
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"))
    colaborador = relationship("Colaborador", back_populates="pontos")

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
