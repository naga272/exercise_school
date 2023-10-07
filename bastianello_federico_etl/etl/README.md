# ETL 3.x
![Language](https://img.shields.io/badge/Spellcheck-Pass-green?style=flat) ![Platform](https://img.shields.io/badge/OS%20platform%20supported-Windows-green?style=flat)![Platform](https://img.shields.io/badge/OS%20platform%20-Windows-green?style=flat) 
![Language](https://img.shields.io/badge/Language-Python-yellowgreen?style=flat)  ![Testing](https://img.shields.io/badge/PEP8%20CheckOnline-Passing-green) ![Testing](https://img.shields.io/badge/Test-Pass-green)

## Descrizione
Il programma allinea.cmd, passatogli come parametro "prima" o "dopo" avvia una serie di programmi (pipeline). Se l'utente ha scritto come parametro prima allora allinea.cmd avvierà il programma python sync.py che prende come parametri tre percorsi di file csv, i primi due di input e l'ultimo di output (chiamato sync.csv e lo inserisce all'interno della cartella flussi). L'output del programma sync.py dipende dal parametro passato a allinea.cmd. Se ad allinea.cmd abbiamo passato come parametro prima, allora il programma python restituirà un file batch chiamato mov.bat (all'interno della directory chiamata bat). Questo file contiene tutti gli studenti di quinta che sono stati promossi e che devono essere spostati nell'organizzazione /studenti.diplomati. In più, il programma sync.py carica all'interno della cartella analisi un file chiamato "quinta.png" che mostra quanti studenti sono stati spostati nella organizzazione /studenti.diplomati rispetto al totale di tutti gli studenti presenti nel file. Dopodichè quando il programma è terminato, allinea.cmd avvia il programma mov.bat che contiene le istruzioni effettive per spostare gli studenti di quinta rilevati dal file cvs nell'organizzazione /studenti.diplomati. 
Invece, se al programma allinea.cmd si passa come parametro dopo, sync.py produrrà tre file (sync.csv, creategsuite.bat e deletegsuite.bat). Il programma sync.py controlla se nel file 77_SIGMA_EXPORT_ALUNNI.csv ci sono studenti che non compaiono in 77_gusers_export_alunni.csv. Poi fa la stessa verifica controllando se in 77_gusers_export_alunni.csv ci sono studenti che non compaiono in 77_SIGMA_EXPORT_ALUNNI.csv. Viene poi generata all'interno della cartella analisi il file "numero_user.png", che dimostra quanti utenti ci sono rispettivamente nei due file passati come input e la differenza tra i due. Invece, all'interno della directory bat vengono creati i file creategsuite.bat (che consente di aggiungere studenti alla gsuite) e deletegsuite.bat (che consente di eliminare studenti dalla gsuite). Il programma sync.py scrive a ogni esecuzione nel file trace.csv chi esegue il programma, con quale pc e a che ora. quando il programma è terminato, allinea.cmd esegue prima il file creategsuite.bat e poi deletegsuite.bat

## Requisiti
- python versione 3.11
- moduli per python non standard come:

|_nome_|        |_versione_|
matplotlib         3.8.0
numpy              1.25.0
pandas             2.1.1
(fare riferimento al file requirements.txt)
## Esecuzione
Eseguire il programma da terminale passando come parametro al file allinea.cmd il parametro prima oppure dopo
## Tags
sys time argparse os re platform try except with open EXIT_SUCCESS EXIT_FAILURE ArgumentParser _exit perror None void append return write localtime strftime time node environ pandas matplotlib platform

## Author
Bastianello Federico
