
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
    * date:        19 / 11 / 2023
    * descrizione: programma  sync.py che scorre i file contenuti nella cartella
    *              repo e produce l'unico file usbdviewall.csv con il contenuto di tutti i file trovati.
    *
"""


def scorri(percorso:str) -> int:
    '''
        *
        *  Funzione che scorre i file contenuti nella cartella passata come paramtro e produce l'unico
        *  file usbdviewall.csv con il contenuto di tutti i file trovati.
        *
    '''
    try:
        f_out           = fopen(strcat(percorso, "usbdviewall.csv"), "w")
        file_analizzati = -1 # parto da -1 perchè considererà anche il file usbdviewall.csv 

        for dirpath, dirnames, filenames in os.walk(percorso):
            for element in filenames: # per ogni file all'interno della cartella
                file_analizzati += 1
                if element != "usbdviewall.csv":
                    printf(f"lettura del file: {element}")
                    with open(strcat(percorso, element), "r") as f_in:
                        for row in f_in:
                            fprintf(f_out, f"{row}")
                    printf(f"fine lettura del file: {element}")

        printf(f"numero di file analizzati: {file_analizzati}")
        fclose(f_out)
        return EXIT_SUCCESS

    except Exception as e:
        perror(f"{e}")
        return EXIT_FAILURE


def main(argc:int, argv:list):
    if argc != 2:
        perror("errore nel passaggio dei paramtri al programma")
        return EXIT_FAILURE

    scorri(argv[1])
    return EXIT_SUCCESS


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
