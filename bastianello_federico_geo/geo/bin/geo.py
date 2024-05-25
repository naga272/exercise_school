from log import *
import requests
import json


def start_page_html():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Geo</title>
            <meta charset='UTF-8'>
            <meta name='viewport' content='device=width-device, initial-scale=1.0'>
            <meta name='author' content='Bastianello Federico'>
            <link rel='StyleSheet' href='#'>
            <style></style>
        </head>
        <body>
    """


def end_page_html():
    return """
            <script></script>
        </body>
    </html>
    """


def dms_to_dd(degrees:int, minutes:int, seconds:int, direction:str):
  """
  Converte le coordinate GPS da DMS a DD.

  Args:
    degrees: Gradi (valore intero).
    minutes: Minuti (valore intero).
    seconds: Secondi (valore float).
    direction: Direzione ('N', 'S', 'E' o 'W').

  Returns:
    Latitudine o longitudine decimale (float).
  """

  dd = float(degrees) + float(minutes) / 60 + seconds / 3600

  if direction in ['S', 'W']:
    dd *= -1

  return dd


def clear(to_clean):
    clean = ""
    for i in range(0, len(to_clean), 1):
        if to_clean[i] != "°" and to_clean[i] != "'" and to_clean[i] != "′":
            clean += to_clean[i]
        else:
            clean += " "

    return clean


def get_json(lati, long):
    url = f"https://api.opentopodata.org/v1/srtm30m?locations={lati},{long}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print("Errore nella richiesta:", response.status_code)


def main(argc:int, argv:list) -> int:
    if argc != 2:
        print("errore durante il passaggio dei parametri da CLI:\n{argv}")
        return 1

    f_in = open(argv[1], "r", encoding="utf-8")
    f_out = open("../web/result.html", "w", encoding="utf-8")
    f_out.write(start_page_html())
    
    f_out.write("\n<table>")
    f_out.write("\n<tr><th>citta</th><th>altitudine</th></tr>")
    for line in f_in:
        f_out.write("\n<tr>")

        f_out.write("\n<td>")
        f_out.write(line.split(";")[0])
        f_out.write("\n</td>")

        line_splitted = line.split(";") 
        first = line_splitted[2].replace("\"", "")
        try:
            second = line.split(";")[3].replace("\"", "") 
        except Exception:
            first = line_splitted[1].replace("\"", "")
            second = line.split(";")[2].replace("\"", "")

        first = clear(first).strip().split()
        second = clear(second).strip().split()

        latitudine = dms_to_dd(int(first[0]), int(first[1]), float(first[2]), str(first[3]))
        longitudine = dms_to_dd(int(second[0]), int(second[1]), float(second[2]), str(second[3]))

        answer_api = get_json(latitudine, longitudine)
        f_out.write("\n<td>")
        f_out.write(str(answer_api["results"][0]["elevation"]))
        f_out.write("\n</td>")
        f_out.write("\n</tr>\n")

    f_out.write("\n</table>")

    f_out.write(end_page_html())
    f_in.close()
    f_out.close()

    return 0


if __name__ == "__main__":
    Log().logMe("programma avviato")
    result = main(len(sys.argv), sys.argv)
    Log().logMe(f"programma terminato con valore: {result}")
    sys.exit(result)
