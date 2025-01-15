
from sqlalchemy                 import create_engine, Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker, relationship


engine = create_engine('sqlite:///local_contravvenzioni.sqlite', echo=True)
Base = declarative_base()


class VigileDB(Base):
    __tablename__ = 'vigile'
    id          = Column(Integer, primary_key=True)
    matricola   = Column(String(20), unique=True)
    nome        = Column(String(100))
    cognome     = Column(String(100))

    def __repr__(self):
        return f"<VigileDB(matricola={self.matricola}, nome={self.nome}, cognome={self.cognome})>"


class AutoDB(Base):
    __tablename__ = 'auto'
    id = Column(Integer, primary_key=True)
    targa = Column(String(10), unique=True)
    marca = Column(String(50))
    modello = Column(String(50))
    proprietario = Column(String(100), default="Non presente")

    def __repr__(self):
        return f"<AutoDB(targa={self.targa}, marca={self.marca}, modello={self.modello})>"


class ContravvenzioneDB(Base):
    __tablename__   = 'contravvenzione'
    id              = Column(Integer, primary_key=True)
    vigile_id       = Column(String(20), ForeignKey('vigile.matricola'))
    auto_id         = Column(String(10), ForeignKey('auto.targa'))
    luogo           = Column(String(200), default="Errore")
    datetime        = Column(String(200))
    tipo_infrazione = Column(String(100))
    importo         = Column(DECIMAL(10, 2), default=200.00)

    vigile = relationship("VigileDB")
    auto = relationship("AutoDB")

    def get_num_campi(self):
        return 6    # la faccio semplice

    def __repr__(self):
        return f"<ContravvenzioneDB(id={self.id}, auto_id={self.auto_id}, vigile_id={self.vigile_id})>"


class LogDB(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    descrizione_evento = Column(String(200))
    datetime = Column(String(200))

    def __repr__(self):
        return f"<LogDB(id={self.id}, descrizione_evento={self.descrizione_evento})>"


# Creazione delle tabelle nel database
Base.metadata.create_all(engine)

# Creazione di una sessione per interagire con il database
Session = sessionmaker(bind=engine)
session = Session()