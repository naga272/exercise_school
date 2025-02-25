# CMDB

## Descrizione

Questo progetto è un web server che raccoglie periodicamente informazioni sul sistema in cui è in esecuzione utilizzando **WMI**.  
Un **thread dedicato** esegue la raccolta ogni **due minuti**, salvando i dati nel database `db.sqlite3`.  

Per visualizzare le informazioni raccolte, basta aprire la homepage:  
[`http://<ip>:<porta>`](http://<ip>:<porta>)

## Requisiti

- **Sistema operativo:** Windows (necessario per il funzionamento di WMI)  
- **Python:** Versione **3.12** o superiore  

## Esecuzione

### Avviare il server

Aprire un terminale nella stessa directory di `manage.py` ed eseguire:  

```sh
python3 manage.py runserver
```

Una volta avviato il server, aprire un browser e visitare:
http://127.0.0.1:8000

### Creare un superuser

Per accedere all'interfaccia di amministrazione e visualizzare il database (/admin), eseguire:

```sh
python3 manage.py createsuperuser
```

## author

- Bastianello Federico
