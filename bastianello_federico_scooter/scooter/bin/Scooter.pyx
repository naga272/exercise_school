
# moduli cython
cimport cython                                         # la uso per i decoratori boundscheck e wraparound
from    libc.stdlib cimport EXIT_SUCCESS, EXIT_FAILURE # prendo le macro e funzioni dall'header stdlib


# moduli standard
from datetime import datetime
import platform
import time
import sys
import os


"""
    *
    * esperimento con la classe Scooter:
    * Oltre a creare la classe Scooter provare quando possibile di alleggerire il programma tramite cython
    * 
    *
"""


@cython.boundscheck(False) # disabilito controllo sugli array di python
@cython.wraparound(False)  # disabilito controllo sugli indici negativi
cdef class Scooter:
    
    all = []

    cdef public: # dichiarazione variabili
        float           _capacita, _quantita_carburante, _resa, _km_percorsi
        unsigned int    _codice


    def __cinit__(self, capacita, resa):
        # sono obbligato ad usare la lista per ottenere l'id perchè in cython non si possono creare delle variabili private in una classe 
        ''' uso cinit al posto di init perche cosi posso lavorare sulle variabili dichiate con cdef'''
        
        try:
            Scooter.all.append(self)
            self._codice                = len(Scooter.all) 

            self._capacita              = capacita
            self._resa                  = resa
            self._quantita_carburante   = 0
            self._km_percorsi           = 0
        
        except Exception as e:
            print(f"{e}") # prevedo il caso in cui si tenti di passare valori non validi
            sys.exit(EXIT_FAILURE)


    def __str__(self) -> str:
        return f"Scooter {self._codice}: Carburante = {self._quantita_carburante}L, KM percorsi = {self._km_percorsi}km"


    def __del__(self):
        print("object destroyed")


    '''
        *
        * I metodi che hanno la seguente sintassi:
        * cdef rifornimento(argv)
        * Non sono visibili esternamente, per questo uso def
        *
    '''
    """ METODI DI CLASSE """
    def rifornimento(self, litri):
        '''
            *
            *  funzione che serve per aggiungere carburante al serbatoio
            *
        '''
        if self._quantita_carburante + litri <= self._capacita:
            self._quantita_carburante += litri


    def avanza(self, distanza):
        '''
            *
            *  funzione che data la distanza da percorrere, riduce la quantità di 
            *  carburante nel serbatoio a seconda della resa e aggiorna il valore del 
            *  contachilometri
            *
        '''
        if self._quantita_carburante > 0:
            km_possibili = self._quantita_carburante * self._resa
            if distanza <= km_possibili:
                self._quantita_carburante -= distanza / self._resa
                self._km_percorsi += distanza


    def reset_km(self):
        '''
            *
            *  Funzione che azzera il contachilometri
            *
        '''
        self._km_percorsi = 0


    """ GETTER """
    @property
    def num_scooters(self)  ->  int:
        return len(Scooter.all)


    @property
    def codice(self)        ->  int:
        return self._codice



"""
    *
    * functions usate per la creazione del file csv log
    *
"""
cdef unsigned short int f_exist(percorso):
    return 1 if os.path.exists(percorso) else 0


def log(percorso:str, file_py:str) -> int:
    try:
        if f_exist(percorso) == 0:
            f_out = open(percorso, "a")
            f_out.write(f"user;pc;versione_python;Nome_file;timestamp;localtime;\n")
        else:
            f_out = open(percorso, "a")

        f_out.write(f"{os.environ['USERNAME' if platform.system() == 'Windows' else 'USER']};{sys.version};{os.path.abspath(__file__)};{str(time.time())};{datetime.now()};\n")
        f_out.close()
        return EXIT_SUCCESS

    except Exception as e:
        print(f"function log - error: {e}")

    f_out.close()
    return EXIT_FAILURE

