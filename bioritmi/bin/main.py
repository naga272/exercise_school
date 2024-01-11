
from stdhtml import *               # contiene la struttura standard di una pagina html, l'ho messo in questo modulo
                                    # per non avere tra i piedi quelle stringhe lunghe e brutte da vedere


# moduli per l'analisi dati
import pandas as pd                 # pip install pandas, lo uso per generare i dataframe, nel programma gli do come alias "pd"
import matplotlib as mpt            # pip install matplotlib, lo uso per i grafici
import matplotlib.pyplot as plt     # fa sempre parte del modulo matplotlib, lo uso per i grafici
import numpy                        # pip install numpy, lo uso per svolgere maggiori operazioni matematiche
import nltk                         # pip install nltk, lo uso come analizzatore sintattico, viene usato per la costruzione di linguaggi


"""
    *
    *   Dopo aver scaricato queste librerie bisogna aggiungere nel pacchetto tramite il comando:
    *   pip freeze > requirements.txt
    *   questo comando inserisce all'interno del file requirements.txt tutti i moduli che abbiamo installato con pip (compresa la versione)
    *   così il proff può scaricare velocemente tutto ciò che gli serve per usare il programma
    *   (togli a mano le librerie che non c'entrano nulla con il programma)
    *
"""


#standard moduli
from datetime import datetime       # lo uso per il log
import platform
import time
import sys
import os
import re                           # mi consente di generare delle regole di sintassi per le stringhe


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def name_user() -> str:
    """ 
        *
        * uso questa funzione per capire che sistema operativo l'utente sta usando
        * così, posso sapere che variabile d'ambiente chiamare in base al so
        *
    """

    match platform.system():
        case "Windows":     # caso sistema operativo windows -> per recuperare il nome utente la variabile di ambiente si chiama USERNAME
            return "USERNAME"
        
        case "Linux":       # caso sistema operativo Linux -> per recuperare il nome utente la variabile di ambiente si chiama USER
            return "USER"

        case _:             # caso di default
            return "ERROR"



def log(percorso_log:str, nome_programma:str) -> int:
    """
        *   Argv:
        *       - percorso_log:   indica dove andare a scrivere il file di log
        *       - nome_programma: indica il nome del programma che si è andati a eseguire
        *
    """
    try:
        intestazione_flag = 0 # lo uso per capire se il file csv ha bisogno di intestazione

        if os.path.exists(percorso_log) == False:
            # se non esiste il file percorso_log dico di cambiare il flag
            intestazione_flag = 1

        with open(percorso_log, "a") as logger:
            if intestazione_flag == 1: # inserisco l'intestazione al file csv
                logger.write(f"user;name_pc;version_python;name_program;timestamp;localtime;\n")

            #scrittura sul file log appena creato
            logger.write(f"{os.environ[name_user()]};{platform.node()};{sys.version};{nome_programma};{time.time()};{datetime.now()};\n")
        
        return EXIT_SUCCESS # comunico che la funzione e' stata eseguita senza problemi
    except Exception as e:  # eccezione nel caso in cui il programma non e riuscito a creare la funzione log
        print(f"{e}")         # visualizzo il problema {l'errore}
        return EXIT_FAILURE # comunico che la funzione ha avuto dei problemi, di consguenza il programma terminerà con un risultato negativo


def create_html(dataframe:object, percorso_x_fileHtml:str) -> int:
    """
        *
        *  Funzione che crea una pagina html
        *
    """
    try: # in caso che sia un percorso non valido si attiva l'errore
        with open(percorso_x_fileHtml, "w") as fhtml:
            fhtml.write(start_html + dataframe.to_html() + fine_html)
        return EXIT_SUCCESS

    except Exception as e:
        print(f"{e}")
        return EXIT_FAILURE


def main(argc:int, argv:list) -> int:
    """
        *
        *   Argv di main:
        *       - argc: numero di argomenti passati da linea di comando (quindi la quantita), 
        *               posso usarlo per verificare quanti parametri un utente mi passa al programma 
        *       - argv: lista di stringhe che contiene tutti i parametri passati al programma,
        *               ad argv[0] si trova sempre il nome del programma python, poi tutti i parametri
        *               
    """
    # argv[1] indica il percorso del file csv da analizzare
    # argv[2] indica in che cartella inserire il file html

    if argc != 3: # se il programma non ha il numero giusto di parametri  
        print("errore nel passaggio degli argomenti al programma") 
        return EXIT_FAILURE

    try:
        df = pd.read_csv(argv[1], sep=",")   # generazione del Dataset prendendolo da un file csv che ha come separatori le "," con pandas (alias pd)
        df.columns = ["matricola", "cognome", "nome", "data", "classe", "sezione"] # aggiungo l'intestazione per ogni colonna del dataset
        print(df)   # visualizzo il dataframe df, dopo lo trasformerò in una tabella html usando il metodo to_html()
        # gli dico di ritornare il valore 0 se la funzione create_html ritorna valore 0, altrimenti la funzione main comunica un errore 
        return EXIT_SUCCESS if create_html(df, argv[2]) == EXIT_SUCCESS else EXIT_FAILURE
    
    except Exception as e: # in caso che sia un percorso non valido si attiva l'errore
        print(f"errore nella funzione main: {e}")
        return EXIT_FAILURE


if __name__ == "__main__":
    result = EXIT_FAILURE
    if log("../log/trace.csv", "python.py") == EXIT_SUCCESS:
        result = main(len(sys.argv), sys.argv)

    print(f"uscita dal programma con valore {result}") # stampo a schermo il valore di uscita del programma

    ''' 
        *
        * quando termina il processo con lo stato 0 (rappresentato con EXIT_SUCCESS), 
        * si indica che l'esecuzione e' andata a buon fine. 
        * sys.exit() e' la procedura (procedura significa funzione che non ritorna valori) 
        * che fa terminare il programma comunicando al s.o. il valore di uscita del programma 
        *
    '''
    sys.exit(result)


"""
    In pratica, la parte if __name__ == "__main__" simula l'inizio di 
    un programma assembly o di un programma C:

    programma assembly (per compilatore nasm) architettura x64bit Kali Linux:

    section .data       ; dichiarazione variabili
        result db 1     ; assegno alla variabili result il valore di uscita 1

    section .text
        global _start   ; indica che il programma parte da _start

    _start:             ; equivalente dell'if __name__ == __main__
        call main
        mov [result], rax ; assegno a result il valore di uscita da main 


    ; il pezzo che segue ora sara la preparazione della funzione sys.exit(result)
    _exit:  mov rax, 60         ; codice per chiamata di sistema
            mov rdi, [result]   ; rappresenta il valore di result (quindi 0)
            syscall             ; chiamata di sistema (il programma termina in questo punto)



    main:   push    rbp             ; equivalente della "def main() -> int:" senza passaggio di parametri
            mov     rbp, rsp

            ;codice dela funzione main

            mov     rax, 0          ; ritorno dalla funzione main 0

            pop     rbp
            ret                     ; uscita dalla funzione main

"""


