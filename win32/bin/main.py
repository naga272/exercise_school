from sqlalchemy import create_engine, inspect, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

from log import Log
import wmi
import sys


class Product():
    Base = declarative_base()
    def __init__(self, product, db_path = "../flussi/wmi32.db"):
        try:
            self.__engine           = create_engine(f"sqlite:///{db_path}")
            self.__session          = sessionmaker(bind = self.__engine)()

            self.__nameProduct      = product.Name
            self.__versionProduct   = product.Version
            self.__vendorProduct    = product.Vendor
            Log().logMe("Oggetto Product creato")
        except Exception as e:
            print(f"percorso {db_path} non valido")
            sys.exit(1)

    def pushInDB(self):
        # Crea la tabella se non esiste
        if not inspect(self.__engine).has_table("Product"):
            Product.Base.metadata.create_all(self.__engine)

        # Controllo se il prodotto esiste già nel database
        existing_product    = self.__session.query(ProductDB).filter_by(
            nameProduct     = self.__nameProduct,
            versionProduct  = self.__versionProduct,
            vendorProduct   = self.__vendorProduct
        ).first()

        if existing_product:
            Log().logMe(f"Prodotto già esistente nel database: {self.__str__()}")
        else:
            self.__session.add(ProductDB(self))
            self.__session.commit()
            Log().logMe(f"Prodotto aggiunto al database: {self.__str__()}")

    def get_nameProduct(self):
        return self.__nameProduct

    def get_versionProduct(self):
        return self.__versionProduct

    def get_vendorProduct(self):
        return self.__vendorProduct

    def __str__(self):
        return f"Nome prodotto: {self.__nameProduct}\nVersione: {self.__versionProduct}\nVenditore: {self.__vendorProduct}"

    def __del__(self):
        Log().logMe("Oggetto Product Eliminato")


class ProductDB(Product.Base):
    __tablename__       = "Product"
    id                  = Column(Integer, primary_key=True)
    nameProduct         = Column(String)
    versionProduct      = Column(String)
    vendorProduct       = Column(String)

    def __init__(self, singleProduct:object):
        self.nameProduct    = singleProduct.get_nameProduct() 
        self.versionProduct = singleProduct.get_versionProduct()
        self.vendorProduct  = singleProduct.get_vendorProduct()
        Log().logMe(f"Inserito nuovo oggetto nella tabella Product del db wmi32.db: \n{singleProduct.__str__()}")


def main() -> int:
    # Esegui una query per ottenere tutte le istanze della classe win32_Product
    for product in wmi.WMI().Win32_Product():
        Product(product).pushInDB()
    return 0


if __name__ == "__main__":
    Log().logMe("Inizio programma")
    result = main()
    Log().logMe(f"programma terminato con valore {result}")
