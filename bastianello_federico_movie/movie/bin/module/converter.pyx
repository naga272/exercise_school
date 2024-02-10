
# librerie analisi dati
import  pandas          as pd
import  lxml


# libreria cython
from    libc.stdlib     cimport EXIT_SUCCESS, EXIT_FAILURE, system
cimport cython


# libreria standard
from    time            import time
from    datetime        import datetime

import  subprocess
import  platform
import  sys
import  os


"""
    *
    *   author:         Bastianello Federico
    *   Titol:          from csv to xml and json
    *   description:    Eseguire la conversione dei dati contenuti all'interno di un file csv
    *                   per file xml e json
    *   data:           10 / 02 / 2024
    *
"""


cdef unsigned short int __unix__
cdef unsigned short int __WIN__
cdef unsigned short int __MACoS_

__unix__    = 1 if platform.system() == "Linux"     else 0
__WIN__     = 1 if platform.system() == "Windows"   else 0
__MACoS__   = 1 if platform.system() == "Darwin"    else 0


arc = getattr(platform, "architecture")()[0][:-3] # capisco che architettura si tratta (se una x16, x32 o x64)


@cython.boundscheck(False)
@cython.wraparound(False)
def main(argc:int, argv:list, envp:list):
    '''
        *
        *   Funzione che converte un file csv lo converte in file xml e json
        *
    '''
    if arc == "16" or argc != 4:
        panic()
    try:
        if logging("../log/trace.csv", argv[0]) == EXIT_SUCCESS:

            print("\nlettura da csv in corso...")
            dataframe = pd.read_csv(argv[1], sep = ",")     # ottengo il dataset       

            print("\nconversione in xml in corso...")
            dataframe.to_xml(argv[2])                       # converto il dataframe estratto in xml
        
            print("\nconversione in json in corso...")
            dataframe.to_json(argv[3])                      # converto il dataframe estratto in json

            return EXIT_SUCCESS

    except Exception as e:
        panic()

    return EXIT_FAILURE


@cython.boundscheck(False)
@cython.wraparound(False)
cdef unsigned short int logging(percorso, file_py):
    '''
        *
        *   funzione che logga chi e quando viene avviato il programma 
        *
    '''
    try:
        with open(percorso, "a") as f_out:
            f_out.write(f"{platform.system()};{os.environ['USERNAME' if __WIN__ == 1 else 'USER']};{time()};{datetime.now()};{file_py};{platform.node()};\n")

        return EXIT_SUCCESS

    except Exception as e:
        panic() 
    sys.exit(EXIT_FAILURE)


@cython.boundscheck(False)
@cython.wraparound(False)
cdef void panic():
    '''
        *
        *   - Function for fun:
        *       Il nome e' una citazione di una funzione di un modulo 
        *       che era dentro al codice sorgente pubblicato del kernel di linux.
        *   
        *   Funzione che comunica un messaggio di errore.
        *   compila in base all'architettura della cpu rilevata il programma assembly adeguato per poi eseguirlo.
        *   i programmi assembly sono stati fatti solo per architettura 32-64 bit, quindi per architetture a 16 bit
        *   si comunica un semplice messaggio di errore.
        *   alla fine della comunicazione del messaggio viene terminato il programma
        *
    '''
    if arc in ["32", "64"]:
        if prepara_panic() == EXIT_SUCCESS:
            system(("../bin/module/error_" + arc).encode("utf-8"))
        else:
            print("Errore durante l'esecuzione del programma")
    else:
        print("Errore durante l'esecuzione del programma")

    print("uscita dal programma con valore:", EXIT_FAILURE)
    sys.exit(EXIT_FAILURE)


@cython.boundscheck(False)
@cython.wraparound(False)
cdef unsigned short int prepara_panic(): # function for experiment and fun
    '''
        *
        *   compila un programma assembly in base all'architettura del pc e avvia l'eseguibile 
        *   per comunicare un errore
        *   (le architetture a 16 bit si arrangiano)
        *
    '''
    if "64" in arc or "32" in arc:
        formato     = "elf" + arc
        file_asm    = "../bin/module/error_" + arc + ".asm"

        nasm        = "nasm -f " + formato + " -g " + file_asm
        ld          = "ld " + file_asm.replace(".asm", ".o") + " -o " + file_asm.replace(".asm", "")

    # la funzione system ritorna un intero:
    # 0 (o EXIT_SUCCESS) se il sottoprocesso a esito positivo, 1 (o EXIT_FAILURE) se qualcosa e' andato storto
    # int system(const char*);
    return EXIT_FAILURE if EXIT_FAILURE in [system(nasm.encode("utf-8")), system(ld.encode("utf-8"))] else EXIT_SUCCESS

