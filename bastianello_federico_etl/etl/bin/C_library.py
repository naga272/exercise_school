from time import *
import platform
import sys
import re
import re
import os


'''
    *
    *  EXIT_SUCCESS e EXIT_FAILURE sono due macro dell'ANSI C dell'header stdlib.h.
    *  Rappresentano i valori di uscita di un programma o di una funzione.
    *  La macro EXIT_SUCCESS (ha valore 0) viene usata per indicare che l'uscita da una funzione o
    *  del programma stesso e' andata a buon fine. EXIT_FAILURE (ha valore != 0) rappresenta il caso
    *  in cui l'uscita del programma o dalla funzione non e' andata a buon fine. 
    *
    *  - dichiarazione in #include <stdlib.h>:
    *  
    *  #define EXIT_SUCCESS 0
    *  #define EXIT_FAILURE 1 // il valore dipende dal compilatore, in ogni caso e sempre != 0
    *
'''
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


'''
    *
    *  Uso <None> per rappresentare il void del C Language.
    *  In C void viene usato per indicare l'assenza del ritorno di un valore da una funzione
    *  es:
    *  match = re.search(pattern_matricola, row)
    *  ritorna None se la riga non ha niente in comune con il pattern
    *
'''
void = None


def perror(msg:str):
    '''
        * 
        * Procedura che comunica un messaggio di errore.
        * Argv:
        *     - msg --> type str()
        * 
    '''
    print(f"{msg}")


def printf(strf:str):
    '''
        * 
        * Procedura che stampa in stdout una stringa formattata.
        * Argv:
        *     - strf --> type str() formattata
        * 
    '''
    print(strf)


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
