
''' personal library '''
from ansic import *
import ansic


''' librerie per analisy data'''
import matplotlib as mlp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


''' standard library '''
import platform
import time
import sys
import os
import re


"""
    *
    * author:      Bastianello Federico
    * consegna:    Monitoraggio USB
    * date:        30 / 09 / 2023
    * descrizione: programma usbdview che passato come paramtro il nome di un file csv contenente
    *              un elenco completo dei dispositivi usb che si sono stati collegati a un pc, detecta
    *              tutte le chiavette USB
    *
"""


def grafo(df, graphic_type:str, percorso:str) -> int:
    '''
        *
        *  Argv:
        *    - df:           DataFrame generato con pandas
        *    - graphic_type: serve per realizzare il tipo di grafico (bar, ...) 
        *    - percorso:     Viene specificato dove verrà salvato il file .png
        *
    '''
    try:
        df.plot(kind = graphic_type)
        plt.title("dati generali usb")
        plt.savefig(percorso)
        plt.show()
        return EXIT_SUCCESS

    except Exception as e:
        perror(f"{e}")
        return EXIT_FAILURE


def identify_usb(stri:str) -> int:
    '''
        *
        *  Argv:
        *     - stri: percorso del file csv
        *
        *  Funzione che genera il grafico che mette a confronto il numero di chiavette usb con tutti i dispositivi usb
        *  rilevati. Genera un file chiamato: <timestamp>_usbdviewnohid.csv che contiene tutte le chiavette usb rilevate.
        *
    '''
    counter           = 0
    counter_chiavette = 0

    with open(stri, "r") as f_in, open(f"../flussi/{time.time()}_usbdviewnohid.csv", "w") as f_out:
        for line in f_in:
            counter += 1
            if "HID" in line or line == "":
                continue    
            else:
                fprintf(f_out, str(line.replace("\t", ";")))
                counter_chiavette += 1

    ''' GRAFICO ANALISI DATI'''
    dats = {
        "usb totali registrate" : [counter], 
        "chiavette usb" : [counter_chiavette],
    } # counter e counter_chiavette devono essere per forza all'interno di una lista, richiesto per la creazione di un Dataframe

    if grafo(pd.DataFrame(dats), "bar", f"../analisi/graficousb_{time.time()}.png") != EXIT_SUCCESS:
        return EXIT_FAILURE

    return EXIT_SUCCESS


def main(argc:int, argv:list) -> int:
    '''
        *
        *  Funzione che verifica numero di paramtri passati come argomenti al programma.
        *  Se il numero di argomenti è sbagliato allora esce dalla funzione,
        *  altrimenti esegue la funzione identify_usb()
        *
    '''
    if argc != 2:
        return EXIT_FAILURE

    if identify_usb(argv[1]) == EXIT_SUCCESS:
        return EXIT_SUCCESS

    return EXIT_FAILURE


if __name__ == "__main__":
    if ansic.log("../log/trace.csv", ansic.__FILE__) == EXIT_SUCCESS:
        if main(argc, ansic.argv) == EXIT_SUCCESS:
            printf(f"uscita dal programma con valore: {EXIT_SUCCESS}")
            ansic._exit(EXIT_SUCCESS)
        else:
            printf(f"uscita dal programma con valore: {EXIT_FAILURE}")
    else:
        printf(f"errore nella creazione del log! uscita dal programma con valore: {EXIT_FAILURE}")

    ansic._exit(EXIT_FAILURE)
