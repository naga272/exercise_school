from sqlalchemy     import create_engine, inspect, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from .log            import Log

import platform
import wmi
import sys


"""
* Modulo creato da Bastianello Federico
* Versione: 0.0.1
* DiskDrive(diskdrive: Win32_DiskDrive, db_path:str[optional]) -> None {istanzia oggetto Win32_DiskDrive}
* @pushInDB() -> None {carica istanza all'interno della tabella del db}
* @get_nameDisk() -> str {Restituisce il nome del disco}
* @get_sizeDisk() -> int {restituisce la grandezza del disco}
* @get_sizeDisk() -> str {restituisce la descrizione del disco}
"""


class DiskDrive():
    Base = declarative_base()
    def __init__(self, diskdrive, db_path = "../flussi/wmi.db"):
        try:
            self.__engine        = create_engine(f"sqlite:///{db_path}")
            self.__session       = sessionmaker(bind = self.__engine)()

            self.__nameDisk      = diskdrive.Model
            self.__sizeDisk      = diskdrive.Size
            self.__description   = diskdrive.Description
            Log().logMe("Oggetto DiskDrive creato")
        except Exception as e:
            Log().logMe(f"errore! {e}")
            sys.exit(1)

    def pushInDB(self):
        if not inspect(self.__engine).has_table("DiskDrive"):
            DiskDrive.Base.metadata.create_all(self.__engine)

        # Controllo se il prodotto esiste già nel database
        existing_product    = self.__session.query(DiskDriveDB).filter_by(
            nameDisk    = self.__nameDisk,
            sizeDisk    = self.__sizeDisk,
            description = self.__description
        ).first()

        if existing_product:
            Log().logMe(f"Prodotto già esistente nel database: {self.__str__()}")
        else:
            self.__session.add(DiskDriveDB(self))
            self.__session.commit()
            Log().logMe(f"Prodotto aggiunto al database: {self.__str__()}")

    def get_nameDisk(self) -> str:
        return self.__nameDisk

    def get_sizeDisk(self) -> int:
        return self.__sizeDisk

    def get_description(self) -> str:
        return self.__description

    def __str__(self) -> str:
        return f"Nome Disco: {self.__nameDisk}\nDimensione: {self.__sizeDisk}\nData di installazione: {self.__description}"

    def __del__(self):
        Log().logMe("Oggetto DiskDrive Eliminato")


class DiskDriveDB(DiskDrive.Base):  # Cambiato da DiskDrive.Base a Base
    __tablename__ = "DiskDrive"
    id            = Column(Integer, primary_key=True)
    nameDisk      = Column(String)
    sizeDisk      = Column(String)
    description   = Column(String)
    pcName        = Column(String)

    def __init__(self, disk: object):
        self.nameDisk       = disk.get_nameDisk() 
        self.sizeDisk       = disk.get_sizeDisk()
        self.description    = disk.get_description()
        self.pcName         = platform.node()
        Log().logMe(f"Inserito nuovo oggetto nella tabella DiskDrive del db wmi32.db: \n{disk.__str__()}")
