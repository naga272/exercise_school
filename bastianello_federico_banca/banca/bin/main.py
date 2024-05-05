
from banca import ContoBancario, ContoCorrente, ContoDeposito, ContoDepositoVincolante # non ho capito come funziona
from log import *
import sys


def main(argc:int, argv:list) -> int:
    conto1 = ContoBancario("siebfu3u8hczdcbibceesvs", 1000.0)
    conto2 = ContoCorrente("siebfu3u8hczdcbibceesvs", 1500.0)
    conto3 = ContoDeposito("siebfu3u8hczdcbibceesvs", 1500.0, 2.5, 2)
    conto4 = ContoDepositoVincolante("siebfu3u8hczdcbibceesvs", 1500.0, 3) #non sono riuscito a implementarla

    print(conto1)
    print(conto2)
    print(conto3)
    print(conto4)

    return 0


path_absolute = os.path.join(os.path.abspath('./'), sys.argv[0])

if __name__ == "__main__":
    Log().logMe(f"Programma {path_absolute} avviato")

    result = main(len(sys.argv), sys.argv)
    print("valore di uscita dal programma: ", result)

    Log().logMe(f"Programma {path_absolute} terminato con valore {result}")

    sys.exit(result)
