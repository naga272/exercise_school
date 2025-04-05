
import psutil


def get_active_ports() -> dict:
    """
    * Simulazione della funzionalita' di netcat
    * Funzione che restituisce un dict contenente tutti i servizi in ascolto (con il relativo programma associato)
    *   {
    *       <nome_eseguibile> : <porta>
    *   }
    """
    # lista di oggetti che contiene tutte le connessioni di rete attive
    connections = psutil.net_connections(kind="inet") 

    services = {
        # <porta> : <nome_eseguibile> 
    }

    for conn in connections:
        # conn.laddr contiene indirizzo locale + la porta di scolto
        # conn.status == psutil.CONN_LISTEN mi permette di capire quali sono in ascolto
        if conn.laddr and conn.status == psutil.CONN_LISTEN: 
            port = conn.laddr.port
            pid = conn.pid
            
            if pid:
                process = psutil.Process(pid)
                services[port] = process.name()
            else:
                services[port] = "Unknown"

    return services
