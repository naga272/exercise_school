# Contravvenzioni

![Language](https://img.shields.io/badge/Spellcheck-Pass-green?style=flat)
![Platform](https://img.shields.io/badge/OS%20platform%20supported-Windows-blue?style=flat)
![Language](https://img.shields.io/badge/Language-Python-yellowgreen?style=flat) 
![Testing](https://img.shields.io/badge/PEP8%20CheckOnline-Passing-green)
![Testing](https://img.shields.io/badge/Test-Pass-gree)

## Descrizione

Programma Python che quando (mentre il server è attivo) apre una pagina web in automatico portandoti alla shermata per fare le contravvenzioni. Se il serve non è online, il programma aprirà una shell stile prompt, dove è possibile inserire dei comandi.

## Requisiti

- Python >= 3.10
- librerie secondarie (vedi requirements.txt)

## Esecuzione

Come accennavo precedentemente, ci sono due modi: Via Web e Via Shell locale.
- **Web**: avviare lo script file.bat (consente di avviare il server Django a 127.0.0.1:8000).
Dopodichè, avviare il programma main.py, che in automatico se rileva il server django all'indirizzo 127.0.0.1 sulla porta 8000, aprirà una scheda web all'indirizzo detto precedentemente. Da quella gui è possibile inserire i dati all'interno del db.

- **Shell**: Nel caso in cui il programma non trova il server web Django, avvia una shell locale stile prompt dei comandi. Per aggiungere una contravvenzione bisogna scrivere il seguente comando per la shell:

```bash
>>> push_in_db 19290 WA231AF "Via Pluto" 12/24/33 "Eccesso di Velocita" 125.23
```
ogni argomento del comando push_in_db corrisponde a un campo della tabella Contravvenzioni:

| matricola | targa         | cod_fisc    | luogo         | datetime                    | tipo_infrazione  | importo |
| ------------ | ------------- | -------------- | -------------- | ---------------------------- | ---------------------------- |-----------|
| 19290     | WA231AF | AHBWIDV | "Via Pluto" | 12/24/33                    | "Eccesso di Velocita" | 125.23 |

Ovviamente, dato che se è attiva questa shell il server online è down, allora i dati verranno memorizzati in un db locale (così si possono aggiungere più tardi quando ritorna on il server).


## Note del programmatore

- finire i casi di eccezione per l'input della shell
- estetica fe del sito web Django
- non è ancora stato implementato il modo di caricare i dati del db locale in quello online


## Tag

Django webserver requests sqlAlchemy Parsing Shell


## author

- Bastianello Federico
