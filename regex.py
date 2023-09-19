
"""

                                    REGEX IN PYTHON
    Le regex (dette anche espressioni regolari o regular esxpression)
    vengono usate per formare un modello di ricerca, quindi
    possono essere usate per verificare se all'interno di una stringa c'è il modello di ricerca rishiesto.
    Python a differenza del C ha un modulo (libreria) standard chiamato re. Per importare il modulo si fa:

"""

import re


"""
    Dopo aver importato il modulo re possiamo cominciare ad usare le regex,
    come in questo esempio esempio:
"""

reg1 = re.compile(r"^Questa") # questo e' un modello di ricerca (modello di ricerca detto anche pattern)

if re.search(reg1, "Questa e' una stringa"):
    print("la stringa inizia con \"Questa\"")
else:
    print("non e' stata trovata alcuna corripondenza")


"""

                            FUNZIONI DEL MODULO RE
    Ecco un'elenco di funzioni all'interno della libreria (o modulo) re:


    - re.findall --> ritorna una lista contenente tutti i match:
        text = "ciao come stai? tutto bene"
        pattern = 'o'
        x = re.findall(pattern, text)
        print(x) # x = ['o', 'o', 'o']


    - re.search --> restituisce un oggetto se ha trovato corrispondenza all'interno della stringa col pattern:
        text = "ciao come stai? tutto bene"
        pattern = 'o'
        x = re.search(pattern, text)
        print(x) # x = None se non trova corrispondenza, <re.Match object; span=(3, 4), match='o'> se ha trovato corrispondenza

        se al posto dell'oggetto voglio ottenere il pattern che ho riscontrato della stringa posso usare:
        print(x.group()) # permette di vedere il pattern che ho riscontrato della stringa


    - re.split() --> restituisce un elenco in cui la stringa è stata divisa ad ogni corrispondenza:
        text = "ciao come stai? tutto bene"
        pattern = ' ' # e' uno spazio
        x = re.search(pattern, text)
        print(x) # x = ["ciao", "come", "stai?", "tutto", "bene"]
 

    - re.sub() --> rimpiazza tutti i match con un testo a mia scelta
        text = "ciao come stai? tutto bene"
        pattern = ' ' # e' uno spazio
        x = re.sub(pattern, " ", "/")
        print(x) # x = "ciao/come/stai?/tutto/bene"

"""



"""
                            METACARATTERI
    I metacaratteri sono dei caratteri che hanno delle proprietà particolari.
    Analizzeremo in questa sezioni i casi generali:
    - [] --> significa un set di caratteri, es. con:
            "[a-zA-Z0-9]"
        stiamo dicendo che stiamo cercando all'interno di una stringa un carattere che puo' essere
        un carattere dell'alfabeto (che sia minuscolo che va a-z o che sia maiuscolo che va da A-Z)
        o un carattere numerico (quindi da 0 a 9).
        Quindi:

        text = "ciao come stai? tutto bene"
        pattern = '[a-zA-Z0-9]'
        x = re.findall(pattern, text) # findall ritorna una lista con tutti i match
        print(x) # x = ['c', 'i', 'a', 'o', 'c', 'o', 'm', 'e', 's', 't', 'a', 'i', 't', 'u', 't', 't', 'o', 'b', 'e', 'n', 'e']


    - \ --> Questo è un segnale di sequenza
        questo segnale dice che il prossimo carattere della regex è un carattere speciale (es: \w \W \s \n \t \d):
            \d : significa "qualunque carattere decimale" (quindi da 0 a 9)
            \D : Tutti i caratteri che sono diversi dai caratteri decimali
            \s : qualunque carattere di spazio (spazio, tabulazione ecc..)
            \S : Tutti i caratteri che sono diversi dagli spazi
            \w : Tutti i caratteri alfanumerici (0-9, A-Z, a-z)
            \W : Tutti i caratteri non alfanumerici

    - . --> Il punto significa "tutti i caratteri eccetto il new-line (\n)"
    - ^ --> Significa che la stringa deve COMINCIARE in un determinato modo
    - $ --> Significa che la stringa deve FINIRE  in un determinato modo
    - * --> Siginifica che un carattere si può ripetere 0 o più occorrenze / volte
    - + --> Siginifica che un carattere si può ripetere 1 o più occorrenze / volte
    - ? --> Siginifica che un carattere si può ripetere 0 o 1 volta
    - {n, m} --> al suo interno possiamo indicare quante occorenze precisamente stiamo cercando all'interno di una stringa, es:
    
        r"[A-Z]{5}" --> significa che stiamo cercando dei caratteri maiuscoli che si ripetono 5 volte di seguito (AAAAA - ZZZZZ)
        r"[A-Z]{5,}" --> significa che stiamo cercando dei caratteri maiuscoli che si ripetono 5 o più volte di seguito (AAAAA - ZZZZZZZZ)
        r"[A-Z]{1,5}" --> significa che stiamo cercando dei caratteri maiuscoli che si ripetono dalle 1 alle 5 volte di seguito (A - ZZZZZZZZ)
    - | --> stesso significato dell'or:
        r"A|Z" --> stiamo cercando o una A oppure una Z
    - () --> le tonde vengono usate per raggruppare in più parti la regex, esempio: 

    FUNZIONE PRINTF 
    i casi possibile che accetto dall'utente per il mio linguaggio sono:
    printf("ciao")
    printf(11)
    printf(variabile)
    printf(funzione())
    printf(funzione(a))
    printf(funzione(11, "ciao"))

    Ora creo una regex che mi aiuta a prevedere questi casi, in modo che l'utente scriva solo questo, quindi:

    OR = r'|'
    START_CASE = r'\s*printf\s*\('
    
    CASE_VAR = r'(\s*[A-Za-z\_]+[\w]*\s*)'
    CASE_STR = r'(\s*"[^"]*")'
    CASE_NUM = r'(\d*)'
    three_case = f'({CASE_VAR}|{CASE_STR}|{CASE_NUM})'

    PARAMETRI_FUNCTION = f'({three_case}(,\s*{three_case})*)*'  #(1, 2)
    CASE_FUNCTION = r'(\s*[A-Za-z\_]+[\w]*\s*\(' + PARAMETRI_FUNCTION + '\))' # function()

    END_CASE = r'\)\s*\n*' # rappresenta la fine della printf; 

    reg_x_printf_function = START_CASE + "(" + three_case + OR + CASE_FUNCTION + ")" + END_CASE
    reg_x_printf_function = re.compile(reg_x_printf_function)


    ''' CARATTERISTICHE FUNZIONE GENERALE '''
    reg_is_function = re.compile(f'{CASE_FUNCTION}') # sintassi di una qualunque funzione
"""


"""
                                        ESERCIZI
    livello 1: trovare all'interno della stringa "Non sono ora, né sono mai stato, un membro del partito semidio"
    tutte gli spazi, una volta trovati contarli e dare come output il numero di spazi

    livello 2: verificare che una stringa inserita dall'utente corrisponda a una e-mail
    (6 char iniziali (potrebbe esserci anche un "."), @, n char dopo la @ (inclusi possibili "."),
    e infine .com, .net ecc..)

    livello 3: verificare che una stringa contenga almeno un carattere maiuscolo, uno minuscolo,
    un carattere speciale, un numero e che sia lunga almeno 8 caratteri in totale
    
    livello 4: realizzare una grammatica per assegnazione di dati a una variabile, ricordando che:
    <Key> = <value>

    Il primo char di Key non può essere un numero, non può avere spazi e non può contenere "-", "\", "/", "*" ecc..
    all'interno di questa stringa per semplicità ci deve essere un solo "=".
    Value può essere una stringa (es. "Hello World"), un numero decimale (es. 10) o
    una espressione aritmetica (es. 4 + 5 * 9 / 2)
    
    Tenere in considerazione anche tutti i possibili spazi messi dall'utente
"""
