from datetime import datetime, date
from time import *
import subprocess
import platform
import sys
import os


"""
    *
    *  Created By Bastianello Federico 30 / 09 / 2023
    *  Libreria per rendere la programmazione in python piu C-friendly
    *  Consente di richiamare funzioni e macro dell'ANSI C.
    *  Libreria per versione python >= 3.10 
    *
"""


"""      argv      """

argv = sys.argv
argc = len(argv)


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


def fprintf(file, strf:str):
    '''
        * 
        * Procedura che scrive all'interno del file una stringa formattata.
        *
    '''
    file.write(strf)


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
        *
    '''
    printf(f"{msg}")


''' INTERRUZIONE FORZATA DEL PROGRAMMA '''
def _exit(x:int):
    '''
        *
        *  Funzione che interrompe il programma con valore di uscita x.
        *  Se il valore di x è 0, la terminazione del programma è avvenuta normalmente,
        *
        *  prototype:
        *     void _exit(register int);
        *
    '''
    sys.exit(x)


''' GESTIONE FILE '''
def f_exist(percorso:str) -> int:
    '''
        *
        * Funzione che verifica se un file esiste
        *
    '''
    try:
        if os.path.exists(percorso):
            return 1
    except Exception as e:
        perror(f"{e}")
    return NULL


def fopen(FILE:str, descriptor:str) -> object:
    '''
        *
        * Funzione che apre un file
        *
    '''
    try:
        if f_exist(FILE):
            ptr = open(FILE, descriptor)
            return ptr
        return NULL
    except Exception as e:
        perror(f"{e}")
        return NULL


def fclose(FILE:object):
    '''
        *
        *  Funzione che chiude un file. In caso di errori durante la chiusura interrompe forzatamente il programma
        *
    '''
    try:
        FILE.close()
    except Exception as e:
        perror(f"{e}")
        _exit(EXIT_FAILURE)


def system(argument:list) -> int:
    '''
        *
        * Funzione che passata una lista di comandi come parametro lo esegue su shell
        * Prototype: int system(const char* string);
        * Ritorna EXIT_FAILURE se qualcosa e' andato storto, EXIT_SUCCESS se e' andato tutto bene 
        *
    '''
    try:
        # avvio un nuovo processo con Popen. Mi restituisce un oggetto che rappresenta il processo in esecuzione
        process = subprocess.Popen(argument, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        """
            Argv di Popen:
                - argument: Specifica il programma da eseguire e i suoi argv. Può esssere una stringa oppure una lista
                - stdin, stdout, stderr: Questi parametri specificano i canali di input, output e errori del processo, rispettivamente.
                                         Se non vengono specificati, vengono utilizzati i valori predefiniti.
                - shell: Se impostato su True, il comando viene eseguito tramite una shell del S.O.
        """
        output, error = process.communicate()

        if process.returncode == 0:
            # diciamo che il risultato delle operazioni del processo creato devono essere codificate in UTF-8, perchè di default restituisce una sequenza di byte
            printf(output.decode('utf-8'))  
            return EXIT_SUCCESS
        else:
            # comunicazione dell'errore
            perror("Error:", error.decode('utf-8'))
            return EXIT_FAILURE
    
    except Exception as e:
        # comunicazione caso speciale
        perror(f"Exception: {e}")
        return EXIT_FAILURE


def compiler(file_py:str):
    percorso_python_exe = sys.executable 
    dir_script          = os.path.dirname(sys.executable) + "\\Scripts\\"

    printf(dir_script + "\\Scripts\\")
    system([dir_script + "pip install pyinstaller"]) # installo pyinstaller
    system([dir_script + "pyinstaller", "--onefile", file_py])
    
    return EXIT_SUCCESS



# la funzione log non fa parte del C_Lybrary, solo che l'ho spostata qui dentro perchè mi da
# troppo fastidio vederla nel main
def log(percorso:str, name_file:str) -> int:
    '''
        *
        * Funzione che traccia chi ha eseguito il programma. Scrive all'interno
        * del file trace.log (che si trova all'interno della dir /log) a che ora il programma
        * e' stato eseguito, l'utente che ha eseguito e il nome del pc. In caso di errore
        * ritorna EXIT_FAILURE
        * 
    '''
    try:
        intestazione_flag = 0
        if f_exist(percorso) != NULL:
            intestazione_flag = 1

        with open(percorso, "a") as log:
            if intestazione_flag == 1:            
                fprintf(log, f"user;pc;versione_python;name_program;timestamp;localtime;\n")
            fprintf(log, f"{os.environ['USERNAME']};{platform.node()};{__STDC__};{name_file};{str(time())};{__TIMESTAMP__};\n")
            return EXIT_SUCCESS

    except Exception as e:
        perror(f"{e}")
        return EXIT_FAILURE
