# CMDB, Servizi di Rete e monitoraggio log

## Descrizione
Questo progetto è un'applicazione web realizzata con Django che fornisce informazioni sullo stato del server, in particolare:
- **Monitoraggio dello spazio su disco** (visibile nella homepage `/`)
- **Elenco dei servizi in ascolto sulle porte di rete** (visibile alla pagina `/services/`)
- **Elenco dei log presenti nel file access.log di XAMPP** (visibile alla pagina `/access.log`)

## Requisiti

- python versione > 3.10 (ideale 3.14) 
- installa i pacchetti elencati in requirements.txt


### Avviare il server Django
```bash
python manage.py runserver
```
Ora il sito è disponibile all'indirizzo: **http://127.0.0.1:8000/**


## Funzionalità

### Homepage (`/`) - Monitoraggio Spazio Disco
La homepage mostra un riepilogo dello storico dello spazio disponibile sui dischi del server.

Dati mostrati:
- Nome del disco
- Spazio totale
- Spazio usato
- Spazio libero
- Percentuale di utilizzo

### Pagina `/services/` - Servizi in ascolto
Questa pagina elenca tutti i processi che stanno ascoltando sulle porte di rete.

Dati mostrati:
- Numero della porta
- Nome del servizio associato (es. Apache, MySQL, SSH, ecc.)


### Pagina `/access.log` - monitoraggio file access log
Questa pagina elenca tutti i log presenti all'interno del file access.log (preso dal file access.log di xampp)

Dati mostrati:
- Timestamp
- Path
- query
- response query


## author
- Bastianello Federico
