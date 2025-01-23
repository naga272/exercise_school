
from shell.body import __init__shell

import webbrowser
import requests
import sys


def is_server_reachable(ip_web_site) -> bool:
    try:
        # Se il server risponde con 200 allora restituisco True
        return requests.get(ip_web_site, timeout = 5).status_code == 200

    except requests.exceptions.RequestException as e:
        return False


def main(ip_web_site: str) -> int:
    if is_server_reachable(ip_web_site):
        try:
            webbrowser.open(ip_web_site) # mi apre il browser alla homepage del server

        except Exception as e:
            print(f"Errore durante l'apertura del browser: {e}")
            print("modalita' shell attivata")
            __init__shell()
    else: 
        # si attiva se il server e' down
        print("modalita' shell attivata")
        __init__shell()
    
    return 0


if __name__ == "__main__":
    result = main("http://127.0.0.1:8000")
    sys.exit(result)
