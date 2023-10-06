from datetime import datetime, date
from time import *
import platform
import sys
import os


"""
    *
    *  Created By Bastianello Federico 30 / 09 / 2023
    *  Libreria per rendere la programmazione in python piu C-friendly
    *  Consente di richiamare funzioni e macro dell'ANSI C.
    *
"""


"""      INIZIALIZZAZIONE COSTANTI      """

void = None
NULL = 0


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


global __DATE__, __TIME__, __TIMESTAMP__, __FILE__, __STDC__
__DATE__      = date.today()                            # Data di esecuzione del file sorgente nella forma "yyyy-mm-dd" 
__TIME__      = __DATE__.strftime("%H:%M:%S")           # Ora di esecuzione del file sorgente nella forma "hh:mm:ss"
__TIMESTAMP__ = datetime.now()                          # Data e ora di esecuzione del file
__FILE__      = os.path.abspath(__file__)               # nome corrente del file che si sta eseguendo
__STDC__      = sys.version                             # versione python


global __unix__ , __MacOs__, __WIN__
__unix__  = NULL
__MacOs__ = NULL
__WIN__   = NULL
operative_system = platform.system()
if operative_system == "Windows":
    __WIN__ = 1
elif operative_system == "Darwin":
    __MacOs__ = 1
elif operative_system == "Linux":
    __unix__ = 1


"""      CREAZIONE FUNZIONI C-LIKE       """
def help_C(): # funzione aiuto, da una lista di tutte le cose che questa libreria permette di fare
    stringa = """
                    |__ elenco funzioni __|        
printf(str1, str2) -> stampa stringa formattata
strlen(str1)       -> ritorna la lunghezza di una stringa
strcat(str1, str2) -> ritorna la concatenazione di due stringhe
strcmp(str1, str2) -> ritorna la stringa piu grande
perror(str1)       -> stampa un messaggio di errore
f_exist(str1)      -> verifica che un file esista
system(str1)       -> esegue la stringa str1 su shell
_exit(int)         -> interruzione forzata del programma
                    |__ elenco macro __|
EXIT_SUCCESS       -> uscita da funzione correttamente, 1
EXIT_FAILURE       -> uscita da funzione con errore, 0
void               -> None
NULL               -> ha valore 0
__unix__           -> NULL se il s.o. in cui si esegue il programma non e' unix-like, ritorna 1 se il s.o. corrisponde
__MacOs__          -> NULL se il s.o. in cui si esegue il programma non e' MacOs, ritorna 1 se il s.o. corrisponde
__WIN__            -> NULL se il s.o. in cui si esegue il programma non e' windows, ritorna 1 se il s.o. corrisponde
__DATE__           -> Data di esecuzione del file sorgente nella forma "yyyy-mm-dd" 
__TIME__           -> Ora di esecuzione del file sorgente nella forma "hh:mm:ss"
__TIMESTAMP__      -> Data e ora di esecuzione del file
__FILE__           -> nome corrente del file che si sta eseguendo
__STDC__           -> versione python"""
    print(stringa)


def printf(strf:str):
    '''
        * 
        * Procedura che stampa in stdout una stringa formattata.
        * 
    '''
    print(strf)


''' GESTIONE STRINGHE '''
def strlen(stri:str) -> int:
    '''
        *
        * Funzione che calcola la lunghezza di una stringa
        *
    '''
    return len(stri)


def strcat(str1:str, str2:str) -> str:
    '''
        *
        * Funzione che concatena due stringhe
        *
    '''
    return str1 + str2


def strcmp(str1:str, str2:str) -> str:
    '''
        *
        * Funzione che confronta due stringe e ritorna quella più grande
        *
    '''
    if str1 > str2:
        return str1
    elif str1 < str2:
        return str2
    else:
        return NULL # se le due stringhe sono uguali ritorno NULL


def perror(msg:str):
    '''
        * 
        * Procedura che comunica un messaggio di errore.
        * Argv:
        *     - msg --> type str()
        * 
    '''
    print(f"{msg}")


''' GESTIONE FILE '''
def f_exist(percorso:str) -> int:
    '''
        *
        * Funzione che verifica se il file esiste
        *
    '''
    if os.path.exists(percorso):
        return EXIT_SUCCESS
    perror(f"{percorso} file inesistente")
    return EXIT_FAILURE


def system(string:str) -> int:
    '''
        *
        * Funzione che passatogli un comando cmd come parametro lo esegue su shell
        * Prototype: int system(const char* string);
        * Ritorna EXIT_FAILURE se qualcosa e' andato storto, EXIT_SUCCESS se e' andato tutto bene 
        *
    '''
    try:
        esegui = os.popen(string)
        result = esegui.read()
        return EXIT_SUCCESS
    except Exception as e:
        return EXIT_FAILURE


''' INTERRUZIONE FORZATA DEL PROGRAMMA '''
def _exit(x:int):
    sys.exit(x)


# la funzione log non fa parte del C_Lybrary, solo che l'ho spostata qui dentro perchè mi fa
# sanguinare gli occhi ogni volta che la vedo nel programma main
def log(percorso:str) -> int:
    '''
        *
        * Funzione che traccia chi ha eseguito il programma. Scrive all'interno
        * del file trace.log (che si trova all'interno della dir /log) a che ora il programma
        * e' stato eseguito, l'utente che ha eseguito e il nome del pc. In caso di errore
        * ritorna EXIT_FAILURE
        * 
    '''
    try:
        with open(percorso, "a") as log:
            log.write(f"\nora locale: {__TIMESTAMP__} - timestamp: {str(time())}\nuser: {os.environ['USERNAME']}")
            log.write(f"\nversione python: {__STDC__}")
            log.write(f"\nprogrammi eseguiti: {__FILE__}\n")
            log.write(f"pc: {platform.node()}\n")
        return EXIT_SUCCESS

    except Exception as e:
        perror(f"{e}")
        return EXIT_FAILURE
