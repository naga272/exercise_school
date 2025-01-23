
from sqlalchemy                 import create_engine, Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker, relationship


engine = create_engine('sqlite:///shell/local_db/local_contravvenzioni.sqlite')
Base = declarative_base()


class VigileDB(Base):
    __tablename__   = 'vigile'
    matricola       = Column(String(32), primary_key = True)
    nome            = Column(String(32), nullable = False)
    cognome         = Column(String(32), nullable = False)

    def __repr__(self):
        return f"matricola: {self.matricola}, nome: {self.nome}, cognome: {self.cognome}"


class GuidatoreDB(Base):
    __tablename__   = 'guidatore'
    cod_fisc        = Column(String(32), primary_key = True)
    nome            = Column(String(32), nullable = False)
    cognome         = Column(String(32), nullable = False)

    def __repr__(self):
        return f"cod_fisc: {self.cod_fisc}, nome: {self.nome}, cognome: {self.cognome}"


class AutoDB(Base):
    __tablename__   = 'auto'
    targa           = Column(String(32), primary_key = True)
    colore          = Column(String(32), nullable = False)

    def __repr__(self):
        return f"targa: {self.targa}, colore: {self.colore}"


class ContravvenzioneDB(Base):
    __tablename__       = 'contravvenzione'
    id                  = Column(Integer, primary_key = True, autoincrement = True)  # Nuovo ID univoco
    matricola           = Column(String(32), ForeignKey('vigile.matricola'), nullable = False)
    targa               = Column(String(32), ForeignKey('auto.targa'), nullable = False)
    cod_fisc            = Column(String(32), ForeignKey('guidatore.cod_fisc'), nullable = False)
    tipo_infrazione     = Column(String(256), nullable = False)
    luogo               = Column(String(64), nullable = False)
    datetime            = Column(String(32), nullable = False)
    importo             = Column(Integer, nullable = False)

    # Relazioni
    vigile      = relationship("VigileDB")
    auto        = relationship("AutoDB")
    guidatore   = relationship("GuidatoreDB")

    def get_num_campi(self):
        return 6

    def __repr__(self):
        return f"matricola: {self.matricola}, targa: {self.targa}, cod_fisc: {self.cod_fisc}"


# Creazione delle tabelle nel database
Base.metadata.create_all(engine)


# Creazione di una sessione per interagire con il database
Session = sessionmaker(bind=engine)
session = Session()
