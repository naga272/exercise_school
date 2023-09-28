from C_library import *
import pandas as pd
import numpy as np
from time import *
import argparse
import platform
import sys
import os
import re


"""
    *
    * program name: sync.py
    * Author: Bastianello Federico 
    * Data: 16 / 09 / 2023
    *
    * Descrizione programma:
    * programma che prende da linea di comando tre argomenti, i primi due argomenti usati come input
    * e il terzo come output. Tutti e tre gli argomenti devono essere dei percorsi di file.
    * il programma prende i due primi argomenti passati da linea di comando e li confronta l'uno con l'altro.
    * Quando una matricola non è presente in una dei due file viene inserita nel file di output
    * (che la posizione in cui verra generato dipenderà dal percorso passato come terzo argomento)
    *
    * Versione 2.x
    * creazione del file creategsuite.bat con le istruzioni GAM per aggiungere a GWS gli
    * utenti presenti in anagrafica e non presenti in GSuite
    * creazione del file deletegsuite.bat con le istruzioni GAM per rimuovere da GWS gli
    * utenti presenti in GSuite e non presenti in anagrafica
    *
"""


def log() -> int:
    '''
        *
        * Funzione che traccia chi ha eseguito il programma. Scrive all'interno
        * del file trace.log (che si trova all'interno della dir /log) a che ora il programma
        * e' stato eseguito, l'utente che ha eseguito e il nome del pc. In caso di errore
        * ritorna EXIT_FAILURE
        * 
    '''
    try:
        with open("../log/trace.log", "a") as log:
            user = os.environ['USERNAME']
            ltuple = localtime()
            time_string = strftime("\n%m/%d/%Y, %H:%M:%S", ltuple)
            log.write(f"\n{str(time_string)} - {str(time())}\n")
            log.write(f"user: {user}")
            log.write("\nprogrammi eseguiti: sync.py\n")
            log.write(f"{platform.node()}\n")
        return EXIT_SUCCESS

    except Exception as e:
        perror(f"{e}")
        return EXIT_FAILURE


def estrai_matricole(email:list, char:str) -> list:
    lista = []
    for element in email: 
        lista.append(element.split(char)[0])
    return lista


def main(argc:int, argv:object) -> int:
    try:
        # out ../flussi/sync.csv --> argv.file_out
        df1 = pd.read_csv(argv.filename1) # filename1 ../flussi/77_gusers_export_alunni.csv 1925 row
        df2 = pd.read_csv(argv.filename2) # filename2 ../flussi/77_SIGMA_EXPORT_ALUNNI.csv  1778 row

        nomi1       = df1["Nome"].tolist()
        cognomi1    = df1["Cognome"].tolist()
        matricole1  = estrai_matricole(df1["Email"].tolist(), "@")
        ou1         = df1["OU"].tolist()
        department1 = df1["department"].tolist()

        matricole2  = df2["matr"].fillna(0).tolist()

        for i in range(0, strlen(matricole1), 1):
            matricole1[i] = str(int(matricole1[i]))

        for i in range(0, strlen(matricole2), 1):
            matricole2[i] = str(int(matricole2[i]))

        ''' FILE BATCH '''
        create_gsuite = open("./create_gsuite.bat", "w")
        delete_gsuite = open("./deletegsuite.bat", "w")

        with open(argv.file_out, "w") as f_out: 
            f_out.write(f"matricole;name_file")
            #gam print users > ou
            for i in range(0, strlen(matricole1), 1):
                if matricole1[i] not in matricole2:
                    f_out.write(f"{matricole1[i]}@studenti.marconiverona.edu.it;{argv.filename1}\n")
                    create_gsuite.write(f"REM {cognomi1[i]} {nomi1[i]} creo account nuovo studente di classe {department1[i]}\n")
                    create_gsuite.write(f"ECHO GAM create user {matricole1[i]}@studenti.marconiverona.edu.it firstname \"{nomi1[i]}\" lastname \"{cognomi1[i]}\" password \"xxxxxx\" changepassword on org\studenti\{department1[i]}\n")
                    create_gsuite.write(f"ECHO GAM update user {matricole1[i]}@studenti.marconiverona.edu.it organization department {department1[i]} primary\n")
                    create_gsuite.write("TIMEOUT 3 > NULL\n")
                    create_gsuite.write(f'ECHO GAM update group {department1[i]}@studenti.marconiverona.edu.it add member user {matricole1[i]}@studenti.marconiverona.edu.it\n\n')

            for element in matricole2:
                if element not in matricole1:
                    f_out.write(f"{element}@studenti.marconiverona.edu.it;{argv.filename2}\n")
                    delete_gsuite.write(f"echo GAM delete user {element}@studenti.marconiverona.edu.it\n")

        delete_gsuite.write("pause")
        create_gsuite.write("pause")
        delete_gsuite.close()
        create_gsuite.close()
        return EXIT_SUCCESS

    except Exception as e:
        perror(e)
        return EXIT_FAILURE


if __name__ == "__main__":
    if log() == EXIT_SUCCESS:
        parser = argparse.ArgumentParser()
        parser.add_argument('filename1', type = str)
        parser.add_argument('filename2', type = str)
        parser.add_argument('file_out', type = str)

        argc = 3
        argv = parser.parse_args()

        result = main(argc, argv)
        printf(f"uscita dal programma con valore: {result}")
        sys.exit(result)

    result = EXIT_FAILURE
    perror(f"|__ errore nella scrittura del log __|")
    printf(f"uscita dal programma con valore: {result}")
    sys.exit(result)
