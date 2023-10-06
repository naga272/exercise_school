# librerie di supporto
from ansic import * # per le funzioni
import ansic
# sono obbligato per poter usare le costanti __unix__, __WIN__ ecc... bisogna usare la seguente sintassi: 
# ansiC.__unix__

# librerie per analisi dati (grafici, lavorazione su csv ecc...)
import matplotlib as mlp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# librerie standard
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
    * Data: 03 / 10 / 2023
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
    * Versione 03.0x
    * Produrre il file batch allinea.cmd che permette di elaborare, all'inizio dell'anno scolastico,
    * gli studenti precedentemente diplomati "/studenti/5*" che dovranno essere sposati nella ou /studenti.diplomati
    * L'elaborazione prevede l'esrecuzione a inizio anno del comando GAM
    * GAM print users ou > gusers.csv
    * e la sua successiva, del file, elaborazione per cambiare l'unità organizzativa
    *
"""


def crea_png(df, tipo_grafico:str, percorso:str):
    df.plot(kind = tipo_grafico)
    plt.savefig(percorso) # creo un file png per la visualizzazione del grafico
    plt.show()            # .show() va sempre dopo savefig() perche potrebbe sovrascrivere il grafico


def estrai_matricole(email:list, char:str) -> list:
    lista = []
    for element in email: 
        lista.append(element.split(char)[0])
    return lista


def cast_list(lista:list) -> list:
    # start lista contiene float, ritorno una lista di stringhe
    return [str(int(x)) for x in lista]


def diploma(matricole:list, anno:list) -> int:
    try:
        counter_quinte = 0
        with open("../bat/mov.bat", "w") as diploma:
            diploma.write(f"@echo off\n")
            for x in range(0, strlen(matricole), 1):
                if anno[x] == 5:
                    #GAM update user matricola@marconiverona.edu.it org /studenti.diplomati
                    diploma.write(f"echo GAM update user {matricole[x]}@marconiverona.edu.it org /studenti.diplomati\n")
                    counter_quinte += 1
        ''' GRAFICO PER ANALISI CSV '''
        dats = {
            "origine" : [len(matricole)],
            "5anno" : [counter_quinte]
        }
        crea_png(pd.DataFrame(dats), "bar", "../analisi/quinta.png")
        return EXIT_SUCCESS

    except Exception as e:
        perror(f"{e}")
        return EXIT_FAILURE


def main(argv:object) -> int:
    try:
        if f_exist(argv.filename1) != EXIT_SUCCESS or f_exist(argv.filename2) != EXIT_SUCCESS:
            perror(f"file not found") # se i file da leggere non esistono
            return EXIT_FAILURE

        df1 = pd.read_csv(argv.filename1) # filename1 ../flussi/77_gusers_export_alunni.csv 1925 row
        df2 = pd.read_csv(argv.filename2) # filename2 ../flussi/77_SIGMA_EXPORT_ALUNNI.csv  1778 row
        ''' estrazione delle colonne dei due dataset '''
        nomi1       = df1["Nome"].tolist()
        cognomi1    = df1["Cognome"].tolist()
        matricole1  = estrai_matricole(df1["Email"].tolist(), "@")
        ou1         = df1["OU"].tolist()
        department1 = df1["department"].tolist()

        classi2 = df2["sezione"].tolist()
        matricole2  = df2["matr"].fillna(0).tolist()
        anno = df2["anno_sigla"].fillna(0).tolist()
        
        # casto gli elementi delle due liste, da float a int e poi diventano str
        # da float non posso treasformarle direttamente in str
        matricole1 = cast_list(matricole1)
        matricole2 = cast_list(matricole2)

        if argv.flag == "prima":
            if diploma(matricole2, anno) == EXIT_SUCCESS:
                return EXIT_SUCCESS
            else:
                return EXIT_FAILURE

        elif argv.flag == "dopo":
            ''' GRAFICO PER ANALISI CSV '''
            dats = {
                "gusers" : [len(matricole1)],
                "anagr" : [len(matricole2)],
                "differenza" : [len(matricole1) - len(matricole2)]
            }
            crea_png(pd.DataFrame(dats), "bar", "../analisi/numero_user.png")

            ''' FILE BATCH '''
            create_gsuite = open("../bat/creategsuite.bat", "w")
            delete_gsuite = open("../bat/deletegsuite.bat", "w")

            with open(argv.file_out, "w") as f_out:
                f_out.write(f"matricole;name_file")
                for i in range(0, strlen(matricole1), 1):
                    if matricole1[i] not in matricole2:
                        f_out.write(f"{matricole1[i]}@studenti.marconiverona.edu.it;{argv.filename1}\n")
                        create_gsuite.write(f"REM {cognomi1[i]} {nomi1[i]} creo account nuovo studente di classe {department1[i]}\n")
                        create_gsuite.write(f"ECHO GAM create user {matricole1[i]}@studenti.marconiverona.edu.it firstname \"{nomi1[i]}\" lastname \"{cognomi1[i]}\" password \"xxxxxx\" changepassword on org\studenti\{department1[i]}\n")
                        create_gsuite.write("TIMEOUT 3 > NULL\n")
                        create_gsuite.write(f'ECHO GAM update group {department1[i]}@studenti.marconiverona.edu.it add member user {matricole1[i]}@studenti.marconiverona.edu.it\n\n')

                for element in matricole2:
                    if element not in matricole1:
                        f_out.write(f"{element}@studenti.marconiverona.edu.it;{argv.filename2}\n")
                        delete_gsuite.write(f"echo GAM delete user {element}@studenti.marconiverona.edu.it\n")

            delete_gsuite.close()
            create_gsuite.close()
            return EXIT_SUCCESS

        return EXIT_FAILURE

    except Exception as e:
        perror(e)
        return EXIT_FAILURE


if __name__ == "__main__":
    if log("../log/trace.log") == EXIT_SUCCESS:
        parser = argparse.ArgumentParser()
        parser.add_argument('filename1', type = str)  # ../flussi/77_gusers_export_alunni.csv
        parser.add_argument('filename2', type = str)  # ../flussi/77_SIGMA_EXPORT_ALUNNI.csv
        parser.add_argument('file_out', type = str)   # sync.csv
        parser.add_argument('flag', type = str)       # opzione prima o dopo

        argv = parser.parse_args()
        result = main(argv)
        printf(f"uscita dal programma con valore: {result}")
        ansic._exit(result)

    result = EXIT_FAILURE
    perror(f"|__ errore nella scrittura del log __|")
    printf(f"uscita dal programma con valore: {result}")
    ansic._exit(result)
