# schtasks

![Language](https://img.shields.io/badge/Spellcheck-Pass-green?style=flat) 
![Platform](https://img.shields.io/badge/OS%20platform%20supported-Windows-green?style=flat) 
![Language](https://img.shields.io/badge/Language-Python-yellowgreen?style=flat)  
![Testing](https://img.shields.io/badge/PEP8%20CheckOnline-Passing-green) 
![Testing](https://img.shields.io/badge/Test-Pass-green)


## Descrizione

programma batch schtasks.bat che esegue il programma schtasks.exe e che cattura il suo output all'interno del file tasks.csv. Inoltre, il programma batch esegue lo script schtasks.py che consente di verificare quali programmi nell'ultima esecuzione non sono andati a buon fine (programma che sono dentro alla path \Microsoft\Windows). Oltre a scrivere su un file csv scrive all'interno del file tasks.sql tutti i task filtrati che hanno avuto come ultimo esito dell'esecuzione diverso da 0. il file tasks.sql una volta eseguito inseirsce le task filtrate all'interno della tabella t_tasks del db. 

## Esecuzione

Andare nella directory del progetto chiamata bin e avviare il programma schtasks.bat 

## Requisiti

python 3.x

Leggi requirements.txt per vedere quali librerie non standard servono

## Author

Bastianello Federico