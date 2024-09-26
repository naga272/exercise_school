from typing import Tuple, List
from log import Log
import pandas as pd
import chardet
import sys


def check_par() -> Tuple[int, List[str]]:
    # funzione per controllare il passaggio dei parametri da cli 
    if len(sys.argv) != 3:
        Log().logMe("Errore durante il passaggio di parametri da cli")
        Log().logMe("Programma terminato con valore: 1")
        sys.exit(1)    

    try:    # verifico che il file esista e che non ci siano problemi di percorso
        open(sys.argv[1], "r").close()
    except Exception:
        Log().logMe(f"Errore, impossibile trovare il file {sys.argv[1]}")
        sys.exit(1)    

    return len(sys.argv), sys.argv


def detect_encoding_file(file_path: str) -> str:
    # funzione che identifica l'encoding di file_path  
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result["encoding"]


def find_column(df: object) ->  Tuple[str, str]:
    """
        Funzione che analizza l'intestazione delle colonne (cerca Nome attività e Ultimo esito)
    """
    nome_attivita_col = ""
    esito_col = ""
    for col in df.columns:
        if 'Nome attiv' in col:
            nome_attivita_col = col  # Salva il nome esatto della colonna

    # Trova la colonna che contiene l'esito delle attività (Ultimo esito)
    for col in df.columns:
        if 'Ultimo esito' in col:
            esito_col = col  # Salva il nome esatto della colonna

    return nome_attivita_col, esito_col


def get_intestazione(df) -> str:
    strings = ""
    for columns in df.columns:
        if columns != df.columns[len(df.columns) - 1]:
            strings += "[" + columns + "], "
        else:
            strings += "[" + columns + "]"
    return strings


def get_row(row) -> str:
    return ', '.join(f"\'" + str(value).replace("'", "_") + "\'" for value in row.values)


def main(argc:int, argv:list) -> int:
    df_in = pd.read_csv(argv[1], sep = ",", encoding = detect_encoding_file(argv[1]))

    nome_attivita_col, nome_esito_col = find_column(df_in)

    if nome_attivita_col == "" or nome_esito_col == "":
        Log().logMe("Errore durante l'esecuzione del programma, campi del dataframe non trovati")
        return 1

    # Filtra il DataFrame per trovare le righe che contengono '\\Microsoft\\Windows' nel nome dell'attività e che hanno un esito diverso da 0
    df_filtrato = df_in[(df_in[nome_attivita_col].str.contains(r'\\Microsoft\\Windows')) & (df_in[nome_esito_col] != "0")]

    with open(argv[2], "w") as f_out:
        # per dare contesto al file csv scrivo che cosa indicano i campi del csv
        intestazione = ",".join(name_column for name_column in df_in.columns)
        f_out.write(intestazione)  

        for _, row in df_filtrato.iterrows():
            # df_filtrato.iterrows() restituisce le righe del Dataframe sottoforma di tuple (indice, riga)
            # _ è un'indice, che però non mi serve in questo caso
            # row rappresenta la singola riga del df
            row_str = ','.join(str(value) for value in row.values) # Converto la riga in una stringa separata da virgole
            f_out.write(f"{row_str}\n")

            with open("./tasks.sql", "w") as fsql:
                for _, row in df_filtrato.iterrows():
                    fsql.write(f"INSERT INTO t_tasks ({get_intestazione(df_filtrato)})\n".replace("�", ""))
                    fsql.write(f"VALUES ({get_row(row)});\n\n".replace("�", ""))
    return 0


if __name__ == "__main__":
    Log().logMe("Programma avviato")
    
    argc, argv = check_par() 
    result = main(argc, argv)

    Log().logMe(f"Programma terminato con valore: {result}")
    sys.exit(result)
