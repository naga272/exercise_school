import geocoder
import requests
import json


def ottieni_dati_meteo(città, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={città}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        dati_meteo = response.json()
        return dati_meteo
    else:
        print("Errore nella richiesta:", response.status_code)
        return None


def stampa_dati_meteo(dati_meteo):
    if dati_meteo:
        nome_città = dati_meteo['name']
        descrizione = dati_meteo['weather'][0]['description']
        temperatura = dati_meteo['main']['temp']
        umidità = dati_meteo['main']['humidity']
        velocità_vento = dati_meteo['wind']['speed']
        print(f"Meteo a {nome_città}:")
        print(f"Descrizione: {descrizione}")
        print(f"Temperatura: {temperatura}°C")
        print(f"Umidità: {umidità}%")
        print(f"Velocità del vento: {velocità_vento} m/s\n\n")
    else:
        print("Impossibile stampare i dati: dati meteo non disponibili.")


def memorizza_csv(dati_meteo):
    with open("../flussi/meteo.csv", "a") as csv:
        for element in dati_meteo.keys():
            csv.write(str(dati_meteo[element]))
            csv.write(";")
    return 0


def memorizza_json(dati_meteo):
    with open("../flussi/meteo.json", "a") as file:
        json.dump(dati_meteo, file)
    return 0



def get_location(latitude, longitude):
    g = geocoder.osm([latitude, longitude], method='reverse')
    return g.json


def main():
    api_key = "c66e5643579160d1a33ffce684e0b525"

    with open("../flussi/citta.csv", "r") as f_in:
        citta = f_in.read().strip().split(";")
    
    for city in citta:
        dati_meteo = ottieni_dati_meteo(city, api_key)
        stampa_dati_meteo(dati_meteo)
        longitudine = dati_meteo['coord']['lon'] # Accesso alla longitudine        
        latitudine = dati_meteo['coord']['lat'] # Accesso alla latitudine
        print(get_location(latitudine, longitudine))
        memorizza_csv(dati_meteo)
        memorizza_json(dati_meteo)


if __name__ == "__main__":
    main()
