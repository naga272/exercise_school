from time import *
import argparse
import platform
import sys
import re
import os


"""
    *
    * program name: sync.py
    * Author: Bastianello Federico 
    * Data: 16 / 09 / 2023
    *     
    * Descrizione programma:
    * programma che prende da linea di comando tre argomenti, i primi due argomenti sono usati come input
    * e il terzo come output. Tutti e tre gli argomenti devono essere dei percorsi di file.
    * il programma prende i due primi argomenti passati da linea di comando e li confronta l'uno con l'altro.
    * Quando una matricola non è presente in una dei due file viene inserita nel file di output
    * (che la posizione in cui verra generato dipenderà dal percorso passato come terzo argomento)
    *
"""


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


def log():
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
            # ricavo l'ora locale
            time_stamp = time()
            ora_locale = localtime(time_stamp)
            '''
                ora_locale e' diventata una struct, per accedere ai suo elementi:
                anno = ora_locale.tm_year
                mese = ora_locale.tm_mon
                giorno = ora_locale.tm_mday
                ora = ora_locale.tm_hour
                minuti = ora_locale.tm_min
                secondi = ora_locale.tm_sec
            '''            
            log.write(f"\n{ora_locale.tm_year}/{ora_locale.tm_mon}/{ora_locale.tm_mday} ore: {ora_locale.tm_hour}:{ora_locale.tm_min}:{ora_locale.tm_sec} - {time_stamp}\n")
            # ricavo il nome di chi esegue il programma
            user = os.environ['USERNAME']
            log.write(f"user: {user}")
            log.write("\nprogrammi eseguiti: etl.py\n")
            # nome computer
            log.write(f"{platform.node()}\n") 
        return EXIT_SUCCESS

    except Exception as e:
        perror(f"{e}")
        return EXIT_FAILURE


def perror(msg):
    '''
        * 
        * Procedura che comunica un messaggio di errore.
        * Argv:
        *     - msg --> type str()
        * 
    '''
    print(f"{msg}")


def estrazione(file, pattern):
    '''
        *
        * Funzione che passata un percorso di un file e un pattern 
        * analizza il contenuto del file cercando la matricola che corrisponde al pattern riga per riga.
        * se viene trovata nella riga una corrispondenza con il pattern passato come parametro aggiunge alla
        * lista la matricola che ha individuato.
        * In caso di qualunque tipo di errore questa funzione ritorna come valore
        * EXIT_FAILURE, altrimenti ritorna la lista
        *
        * Argv:
        *    - file --> type str()
        *    - pattern --> type str()
        *
    '''
    try:
        lista = []
        with open(file, "r") as f_in:
            for row in f_in:
                match = re.search(pattern, row)
                if match != void:
                    lista.append(match.group())
            return lista

    except Exception as e:
        perror(e)
        return EXIT_FAILURE


def main(argv):
    '''
        * Argv:
        *    - argv --> object type (argparse.Namespace)
        *
    '''
    try:
        with open(argv.file_out, "w") as f_out:   # ../flussi/sync.csv

            regex = r"\d{5}"
            inp1 = estrazione(argv.filename1, regex)  # argv.filename1 = ../flussi/77_gusers_export_alunni.csv
            inp2 = estrazione(argv.filename2, regex)  # argv.filename2 = ../flussi/77_SIGMA_EXPORT_ALUNNI.csv

            if inp1 == EXIT_FAILURE or inp2 == EXIT_FAILURE:
                perror("qualcosa e' andato storto")
                return EXIT_FAILURE

            f_out.write(f"email;<name_file>\n")
            for matricola in inp1:
                if matricola not in inp2:
                    f_out.write(f"{matricola}@studenti.marconiverona.edu.it;{argv.filename1}\n")

            for matricola in inp2:
                if matricola not in inp1:
                    f_out.write(f"{matricola}@studenti.marconiverona.edu.it;{argv.filename2}\n")

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

        argv = parser.parse_args()

        result = main(argv)
        print(f"uscita dal programma con valore: {result}")
        sys.exit(result)

    result = EXIT_FAILURE
    perror("|__errore nella scrittura del log__|")
    print(f"uscita dal programma con valore: {result}")
    sys.exit(result)
