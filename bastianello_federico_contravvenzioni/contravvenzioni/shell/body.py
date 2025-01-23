
from shell.local_db.local   import *
from urllib.parse           import quote # lo uso per l'url della RAPI (codifica dell'url) 
from datetime               import datetime
import requests
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
    "contravvenzione" : {
        "flags" : {
            "--help" : "Usato per pushare dati nella tabella Contravvenzioni. \n\tRichiede 6 argomenti: (matricola_vigile, targa, luogo, tipo_infrazione, importo)"
        },
    },
    "push_vigile" : {
        "flags" : {
            "--help" : "Consente l'inserimento di una nuova tupla all'interno della tabella vigile. Gli argomenti sono:\n\tmatricola, nome, cognome"
        }
    },
    "push_auto" : {
        "flags" : {
            "--help" : "Consente l'inserimento di una nuova tupla all'interno della tabella Auto. Gli argomenti sono:\n\ttarga, colore"
        }
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
    },
    "push_on" : {
        "flags": {
            "--help" : "consente di fare lo shutdown del terminale"
        }
    }
}


def push_on(argc: int, argv: list):
    # rapi/<str:mat>_<str:targa>_<str:cod_fisc>_<str:luogo>_<str:dats>_<str:reason>_<float:import>
    if "--help" in argv:
        return command_list["push_on"]["flags"]["--help"]

    # guidatore = session.query(GuidatoreDB).filter_by(cod_fisc = cod_fisc).first()
    for element in session.query(ContravvenzioneDB):
        richiesta   = ''
        auto        = session.query(AutoDB).filter_by(targa = element.targa).first()
        guidatore   = session.query(GuidatoreDB).filter_by(cod_fisc = element.cod_fisc).first()
        vigile      = session.query(VigileDB).filter_by(matricola = element.matricola).first()
        
        try:
            richiesta = "http://127.0.0.1:8000/rapi/"
            richiesta += f"{vigile.matricola}"
            richiesta += f"_{auto.targa}"
            richiesta += f"_{auto.colore}"
            richiesta += f"_{guidatore.cod_fisc}"
            richiesta += f"_{guidatore.nome}"
            richiesta += f"_{guidatore.cognome}"
            richiesta += f"_{quote(element.luogo)}"
            richiesta += f"_{quote(str(element.datetime.replace("/", " ").replace("\\", "")))}"
            richiesta += f"_{quote(element.tipo_infrazione)}"
            richiesta += f"_{element.importo}"

            print("URL inviato:", richiesta)  # Debug
            result = requests.get(richiesta)
            session.delete(element)
            session.commit()

        except requests.exceptions.RequestException as e:
            return f"errore nell'inviare i dati: {e}"

    if result.status_code == 200:
        return 'invio dei dati eseguito con successo'
    else:
        return f"errore nell'inviare i dati {result.status_code}"


def contravvenzione(argc: int, argv: list) -> str:
    if "--help" in argv:
        return command_list["push_in_db"]["flags"]["--help"]

    if argc != ContravvenzioneDB().get_num_campi():  #  e' escluso il comando push_in_db
        return f"""
        Errore: numero di argomenti non valido (inseriti solo {argc}).
        rilevati argomenti: {argv}.
        Sono richiesti {ContravvenzioneDB().get_num_campi()} argomenti: matricola_vigile, targa, luogo, tipo_infrazione, importo.
        """

    try:
        matricola       = str(argv[0])
        targa           = str(argv[1])
        cod_fisc        = str(argv[2])
        luogo           = str(argv[3])
        data            = str(datetime.now())
        tipo_infrazione = str(argv[4])
        importo         = float(argv[5])

        vigile = session.query(VigileDB).filter_by(matricola = matricola).first()
        if not vigile:
            return 'matricola del vigile non riconosciuta'

        auto = session.query(AutoDB).filter_by(targa = targa).first()
        if not auto:
            auto = AutoDB(targa = targa, colore = "Rosso")
            session.add(auto)
            session.commit()


        guidatore = session.query(GuidatoreDB).filter_by(cod_fisc = cod_fisc).first()
        if not guidatore:
            guidatore = GuidatoreDB(cod_fisc = cod_fisc, nome = "Luca", cognome = "Rossi")
            session.add(guidatore)
            session.commit()

        nuova_contravvenzione = ContravvenzioneDB(
            matricola           = vigile.matricola,     # matricola del VigileDB
            targa               = auto.targa,           # targa dell'AutoDB
            cod_fisc            = guidatore.cod_fisc,   # codice fiscale del guidatore
            datetime            = data,
            tipo_infrazione     = tipo_infrazione,
            luogo               = luogo,
            importo             = importo
        )

        session.add(nuova_contravvenzione)
        session.commit()

        return "Contravvenzione inserita correttamente nel database locale."

    except ValueError as e:
        return f"Errore: uno o più argomenti non sono nel formato corretto. Dettagli: {e}"

    except Exception as e:
        session.rollback()  # Annulla la transazione in caso di errore
        return f"Errore durante l'inserimento della contravvenzione: {e}"

    return 'dati salvati correttamente!\n'


def push_vigile(argc: int, argv: list) -> str:
    if "--help" in argv:
        return command_list["set_vigile"]["flags"]["--help"]

    vigile = VigileDB(
        matricola   = argv[0], 
        nome        = argv[1], 
        cognome     = argv[2]
    )
    session.add(vigile)
    session.commit()
    return "Nuovo vigile inserito con successo"


def push_auto(argc: int, argv: list) -> str:
    if "--help" in argv:
        return command_list["set_auto"]["flags"]["--help"]

    auto = AutoDB(
        targa   = argv[0],
        colore  = argv[1]
    )
    session.add(auto)
    session.commit()
    return "Nuova auto inserita con successo"


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
            result += f"\t" + command_list[element]["flags"]["--help"] + "\n"

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
            # result contiene l'output della funzione del comando eseguito
            result = globals() [command_from_prompt[0]](len(command_from_prompt) - 1, command_from_prompt[1::])

            if result != None:
                print(result)

            return 0

    print(f"errore! comando: '{memorize_param}' non riconosciuto! digita \"help\" per conoscere i comandi consentiti")
    return 1


def __init__shell():
    clear(0, [])
    while True:
        command = input(f"{os.getenv('USERNAME')} >>> ").strip()
        check_command(command)


if __name__ == "__main__":
    __init__shell()
