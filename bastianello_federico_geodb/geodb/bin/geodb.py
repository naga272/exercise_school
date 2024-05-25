from log import *
import sys


Base = declarative_base()


class Location():
    def __init__(self, location, provincia, lat, lon, altitudine):
        self.__location = location
        self.__provincia = provincia
        self.__lat = lat
        self.__lon = lon
        self.__altitudine = altitudine

        Log().logMe(f"istanziato oggetto {type(self)}")

    def get_location(self):
        return self.__location

    def get_provincia(self):
        return self.__provincia

    def get_lat(self):
        return self.__lat

    def get_lon(self):
        return self.__lon

    def get_altitudine(self):
        return self.__altitudine

    def __str__(self):
        return f"location: {self.__location} provincia: {self.__provincia} lat: {self.__lat} lon: {self.__lon} altitudine: {self.__altitudine}"

    def __del__(self):
        Log().logMe(f"oggetto eliminato{type(self)}")


class LocationDB(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    location = Column(String)
    provincia = Column(String) 
    lat = Column(Float)
    lon = Column(Float)
    altitudine = Column(Float)
    
    def __init__(self, my_obj):
        self.location = my_obj.get_location()
        self.provincia = my_obj.get_provincia()
        self.lat = my_obj.get_lat()
        self.lon = my_obj.get_lon()
        self.altitudine = my_obj.get_altitudine()


class Percorso():
    tappe = []
    def __init__(self, nome:str, data_inizio:str):
        self.__nome = nome
        self.__data_inizio = data_inizio
        self.__tappe = Percorso.tappe
        Log().logMe(f"istanziato oggetto {type(self)}")

    def get_nome(self) -> str:
        return self.__nome

    def get_data_inizio(self) -> str:
        return self.__data_inizio

    def get_tappe(self) -> object:
        return self.__tappe 

    def __str__(self) -> str:
        f"nome: {self.__nome} data inizio: {self.__data_inizio}\n"


def main(argc:int, argv:list) -> int:
    if argc != 2:
        print(f"errore nel passaggio dei parametri {argv}")
        return 1

    with open(argv[1], "r") as f_in:
        engine = create_engine(f"sqlite:///../db/geodb.db")
        session = sessionmaker(bind = engine)()

        if not inspect(engine).has_table("location"):
            Base.metadata.create_all(engine)

        for row in f_in:
            row_splitted = row.split(";")
            Percorso.tappe.append(row_splitted[0] + row_splitted[1])            
            session.add(LocationDB(Location(row_splitted[0], row_splitted[1], row_splitted[2], row_splitted[3], row_splitted[4])))
            session.commit()

        test = Percorso("Federico", "12-13-1222")
        print("elenco tappe:", test.get_tappe())

    return 0


if __name__ == "__main__":
    Log().logMe("programma avviato")
    result = main(len(sys.argv), sys.argv)
    Log().logMe(f"programma terminato con valore {result}")
    sys.exit(result)
