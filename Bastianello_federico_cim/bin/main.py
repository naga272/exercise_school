
from sqlalchemy import create_engine, inspect, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

from utility.diskdrive      import DiskDrive
from utility.product        import Product
from utility.networkAdapter import NetworkAdapter
from utility.log            import Log

import platform
import wmi
import sys


"""
* Programma creato da Bastianello Federico
* 08 / 10 / 2024
"""


def main() -> int:
    wmi_istance = wmi.WMI()

    # inserisco un oggetto alla volta all'interno della tabella
    for product in wmi_istance.Win32_Product():
        Product(product).pushInDB()

    # inserisco un oggetto alla volta all'interno della tabella
    for disk in wmi_istance.Win32_DiskDrive():
        DiskDrive(disk).pushInDB()

    # inserisco un oggetto alla volta all'interno della tabella
    for scheda in wmi_istance.Win32_NetworkAdapter():
        NetworkAdapter(scheda).pushInDB()

    return 0


if __name__ == "__main__":
    Log().logMe("Inizio programma")
    result = main()
    Log().logMe(f"programma terminato con valore {result}")
