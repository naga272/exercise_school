
from Scooter import *

from datetime import datetime
import platform
import time
import sys
import os
import re


"""
    *
    *  Titolo: scooter
    *  autore: 07 / 01 / 2024
    *
"""




def main(argc:int, argv:list, envp:list) -> int:
    """
        *
        * Funzione per il test della classe scooter
        * spiegazione parametri fun. main:
        *  - argc: numero di argomenti passati al programma
        *  - argv: lista di stringhe passate come parametri al programma
        *  - envp: lista contenente tutte le variabili d'ambiente
        *
    """
    scooter1 = Scooter(6, 30)  # Creazione di uno scooter con capacità 5 litri e resa 30 km/l
    scooter2 = Scooter(6, 25)  # Creazione di uno scooter con capacità 6 litri e resa 25 km/l

    print("Stato iniziale:")
    print(scooter1)
    print(scooter2)
    scooter1.rifornimento(3)  # Aggiunge 3 litri di carburante allo scooter 1
    scooter2.rifornimento(4)  # Aggiunge 4 litri di carburante allo scooter 2

    scooter1.avanza(60)  # Avanza lo scooter 1 di 60 km
    scooter2.avanza(70)  # Avanza lo scooter 2 di 70 km

    print("\nDopo l'avanzamento:")
    print(scooter1)
    print(scooter2)

    scooter1.reset_km()  # Azzeramento dei km percorsi dello scooter 1

    print("\nDopo l'azzeramento dei km percorsi dello scooter 1:")
    print(scooter1)
    print(scooter2)
 
    print(scooter2.num_scooters)
    print(scooter1.codice)

    return 0



if __name__ == "__main__":
    """
        *
        * La '''considero''' come se fosse la funzione _start(), quindi inizializzo i parametri da passare al main,
        * la variabile result contiene il valore di uscita della funzione main, che verrà usato per comunicare
        * in output il valore di uscita del programma.
        *
    """
    result = 1

    if log("../log/trace.csv", __file__) == 0:
        result = main(len(sys.argv), sys.argv, [(key, value) for key, value in os.environ.items()])

    print(f"uscita dal programma con valore: {result}")
    sys.exit(result)

