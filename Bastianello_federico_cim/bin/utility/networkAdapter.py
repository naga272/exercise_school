from sqlalchemy     import create_engine, inspect, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from .log            import Log

import platform
import wmi
import sys


"""
* Modulo creato da Bastianello Federico
* Versione: 0.0.1
* NetworkAdapter(scheda: Win32_NetworkAdapter, db_path:str[optional]) -> None {istanzia oggetto Win32_NetworkAdapter}
* @pushInDB() -> None {carica istanza all'interno della tabella del db}
* @get_name() -> str {Restituisce il nome del disco}
* @get_MACAddress() -> str {restituisce il MAC della scheda di rete}
* @get_description() -> str {descrizione della scheda di rete}
"""


class NetworkAdapter():
    Base = declarative_base()
    def __init__(self, scheda, db_path = "../flussi/wmi.db"):
        try:
            self.__engine        = create_engine(f"sqlite:///{db_path}")
            self.__session       = sessionmaker(bind = self.__engine)()

            self.__name         = scheda.Name
            self.__MACAddress   = scheda.MACAddress
            self.__description  = scheda.Description

            Log().logMe("Oggetto NetworkAdapter creato")
        except Exception as e:
            Log().logMe(f"errore! {e}")
            sys.exit(1)

    def pushInDB(self):
        if not inspect(self.__engine).has_table("NetworkAdapter"):
            NetworkAdapter.Base.metadata.create_all(self.__engine)

        existing_product    = self.__session.query(NetworkAdapterDB).filter_by(
            name            = self.__name,
            MACAddress      = self.__MACAddress,
            description     = self.__description
        ).first()

        if existing_product:
            Log().logMe(f"Prodotto già esistente nel database: {self.__str__()}")
        else:
            self.__session.add(NetworkAdapterDB(self))
            self.__session.commit()
            Log().logMe(f"Prodotto aggiunto al database: {self.__str__()}")

    def get_name(self)              -> str:
        return self.__name

    def get_MACAddress(self)        -> str:
        return self.__MACAddress

    def get_description(self)       -> str:
        return self.__description

    def __str__(self)               -> str:
        return f"Nome scheda: {self.__name}\nMAC: {self.__MACAddress}\nDescrizione: {self.__description}"

    def __del__(self):
        Log().logMe("Oggetto NetworkAdapter Eliminato")


class NetworkAdapterDB(NetworkAdapter.Base):
    __tablename__ = "NetworkAdapter"
    id            = Column(Integer, primary_key=True)
    name          = Column(String)
    MACAddress    = Column(String)
    description   = Column(String)
    pcName        = Column(String)

    def __init__(self, scheda: object):
        self.name           = scheda.get_name() 
        self.MACAddress     = scheda.get_MACAddress()
        self.description    = scheda.get_description()
        self.pcName         = platform.node()
        Log().logMe(f"Inserito nuovo oggetto nella tabella NetworkAdapter del db wmi32.db: \n{scheda.__str__()}")
