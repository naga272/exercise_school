
from shell.local_db.local import *

import platform
import sys
import re
import os


# implemento solo i comandi piu basilari e nel modo piu' semplice possibile
command_list = {
    "help" : {
        "flags" : {

        }
    },
    "push_in_db" : {
        "flags" : {
            "--help" : "Usato per pushare dati nella tabella Contravvenzioni. \n\tRichiede 6 argomenti: (matricola_vigile, targa, luogo, datetime, tipo_infrazione, importo)"
        },
    },
    "clear" : {
        "flags" : {
            "--help" : "consente la pulizia del terminale"
        },
    },
    "exit" : {
        "flags": {
            "--help" : "consente di fare lo shutdown del terminale"
        }
    }
}


def push_in_db(argc: int, argv: list):
    if "--help" in argv:
        return command_list["push_in_db"]["flags"]["--help"]

    # Verifica che il numero di argomenti sia corretto
    if argc != 6:  #  6 perche' e' escluso il comando
        return f"""
        Errore: numero di argomenti non valido (inseriti solo {argc}).
        rilevati argomenti: {argv}.
        Sono richiesti {ContravvenzioneDB().get_num_campi()} argomenti: vigile_id, auto_id, luogo, datetime, tipo_infrazione, importo.
        """

    try:


        # Estrai i valori dagli argomenti
        matricola       = str(argv[0])  # deve essere di tipo str
        targa           = str(argv[1])  # deve essere di tipo str
        luogo           = str(argv[2])  # deve essere di tipo str
        datetime        = str(argv[3])  # deve essere di tipo str
        tipo_infrazione = str(argv[4])  # deve essere di tipo str
        importo         = float(argv[5])  # Converti l'importo in un float

        # Verifica se il VigileDB esiste già nel database
        vigile = session.query(VigileDB).filter_by(matricola = matricola).first()
        if not vigile:
            # Se non esiste, crea un nuovo VigileDB
            vigile = VigileDB(matricola = matricola, nome = "Nome sconosciuto", cognome = "Cognome sconosciuto")
            session.add(vigile)
            session.commit()

        # Verifica se l'AutoDB esiste già nel database
        auto = session.query(AutoDB).filter_by(targa = targa).first()
        if not auto:
            # Se non esiste, crea un nuovo AutoDB
            auto = AutoDB(targa = targa, marca = "Marca sconosciuta", modello = "Modello sconosciuto")
            session.add(auto)
            session.commit()

        # Crea una nuova contravvenzione
        nuova_contravvenzione = ContravvenzioneDB(
            vigile_id=vigile.matricola,  # Uso la matricola del VigileDB esistente o appena creato
            auto_id=auto.targa,  # Uso la targa dell'AutoDB esistente o appena creato
            luogo=luogo,
            datetime=datetime,
            tipo_infrazione=tipo_infrazione,
            importo=importo
        )

        # Aggiungi la contravvenzione al database
        session.add(nuova_contravvenzione)
        session.commit()

        return "Contravvenzione inserita correttamente nel database locale."

    except ValueError as e:
        return f"Errore: uno o più argomenti non sono nel formato corretto. Dettagli: {e}"

    except Exception as e:
        session.rollback()  # Annulla la transazione in caso di errore
        return f"Errore durante l'inserimento della contravvenzione: {e}"

    return ''


def clear(argc: int, argv: list):
    
    if "--help" in argv:
        return command_list["clear"]["flags"]["--help"]
    
    os.system("cls" if platform.system() == "Windows" else "clear")
    return ''


def exit(argc: int, argv: list):
    if "--help" in argv:
        return command_list["exit"]["flags"]["--help"]

    sys.exit()


def help(argc: int, argv: list):
    result = 'elenco comandi shell:\n'
    
    for element in command_list.keys():
        if "--help" in command_list[element]["flags"].keys(): 
            result += f"- {element}:\n"
            result += f"\t{command_list[element]["flags"]["--help"]}\n"

    return result


def clean_command(from_prompt: str):
    """
    Il numero di argomenti che passo al comando determina la quantita' di campi.
    Il problema viene quando un campo e' di tipo varchar e al suo interno contiene degli spazi.
    lo .split() mi divide anche quella frase, aumentando il numero di campi generando così errori. 
    Devo quindi pulire il comando in caso di stringhe prima dello split()
    """
    command_cleaned = []
    dentro_stringa  = False
    argument        = ''
    count_char      = 0

    from_prompt += ' '
    for char in from_prompt:
        if char == '\"':
            if dentro_stringa == True:
                dentro_stringa = False
                if argument != '':
                    # controllo che negli argomenti non sia stata passata una stringa del tipo "" (per sicurezza non voglio dare possibilita' di generare errori)
                    command_cleaned.append(argument)
                    argument = ''
                    count_char = 0
                else:
                    print("errore! hai passato una stringa vuota")
                    return 1    
            else:
                dentro_stringa = True 

        elif (dentro_stringa == True) and (char != '\"'): # sto analizzando dentro la stringa (senza considerare doppi apici)
            argument += char
            count_char += 1

        elif (dentro_stringa == False) and (char != ' '):
            argument += char
            count_char += 1

        elif (dentro_stringa == False) and (char == ' ') and (count_char > 0):
            command_cleaned.append(argument)
            argument = ''
            count_char = 0

    if dentro_stringa == True:
        # l'utente ha inserito una sola ", cosa che non e' possibile (o comunque un numero dispari di '"')
        # una volta che dentro_stringa e' uguale a True, deve poi obbligatoriamente diventare False 
        return 1

    return command_cleaned


def check_command(command_from_prompt: str):
    memorize_param = command_from_prompt # var che uso solo per printare in caso di errore i parametri originali

    if "\"" in command_from_prompt:
        command_from_prompt = clean_command(command_from_prompt)

        if command_from_prompt == 1:
            print(f'errore durante il passaggio dei parametri! {memorize_param}')
            return 
    else:
        command_from_prompt = command_from_prompt.split(" ") if (" " in command_from_prompt) and ("\"" not in command_from_prompt) else [command_from_prompt]

    for element in command_list.keys():

        if element == command_from_prompt[0]:
            # result contiene l'output (stringa) del comando eseguito
            result = globals() [command_from_prompt[0]](len(command_from_prompt) - 1, command_from_prompt[1::])

            # e poi scriverci sopra
            if result != None:
                print(result)

            return 0

    print(f"errore! comando: '{memorize_param}' non riconosciuto! digita \"help\" per conoscere i comandi consentiti")
    return 1


def __init__shell():
    clear(0, [])
    while True:
        command = input(f"{os.getenv("USERNAME")} >>> ").strip()
        check_command(command)


if __name__ == "__main__":
    __init__shell()