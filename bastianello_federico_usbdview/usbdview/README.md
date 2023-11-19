# usbdview
![Language](https://img.shields.io/badge/Spellcheck-Pass-green?style=flat) ![Platform](https://img.shields.io/badge/OS%20platform%20supported-Windows-green?style=flat)![Platform](https://img.shields.io/badge/OS%20platform%20-Windows-green?style=flat) 
![Language](https://img.shields.io/badge/Language-Python-yellowgreen?style=flat)  ![Testing](https://img.shields.io/badge/PEP8%20CheckOnline-Passing-green) ![Testing](https://img.shields.io/badge/Test-Pass-green)

## Descrizione
Realizzare la pipeline usbdview che permetta:
- l'esecuzione dell'applicativo usbdview.exe con export su file usbdview.csv
- implementi il filtro HID tramite il programma usbdview.py del file export usbdview.csv senza i device HID e dia come output il file usb usbdviewnohid.csv
- sposti il file usbdviewnohid.csv nella cartella c:\work\repousb\

### Funzionalità aggiuntiva
Implementare il programma  sync.py che scorre i file contenuti nella cartella repo e produce l'unico file usbdviewall.csv con il contenuto di tutti i file trovati.

## Requisiti
- python versione 3.11
- moduli per python non standard come:

|_nome_| |_versione_|
|pandas| |2.1.1|
|matplotlib| |3.8.0|
|numpy| |1.25.0|
ansic.py -> libreria personale, me la sono creato per fare meno confusione con la sintassi del C e python. Si trova direttamente all'interno della cartella package
all'interno della cartella bin. 
Nella libreria ansic.py c'è una funzione chiamata compiler, che viene usata nel caso in cui si volesse compilare il prgramma python.
Per Far funzionare correttamente questa funzione è necessaria la libreria pyinstaller versione 6.2.0. In automatico la funzione
quando chiamata tenta di scaricare pyinstaller con pip (tramite funzione system sempre del modulo ansic). Sarebbe meglio, per evitare 
eventuali errori del programma comunque averla installata

## Esecuzione
da shell o da script. 

## Tags
EXIT_SUCCESS EXIT_FAILURE __TIME__ __FILE__ _exit printf HTML5 css table td tr pandas read_html argv sys os ansic f_exist NULL except perror read_html to_list

## Author
Bastianello Federico
