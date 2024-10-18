

"""
    Mi da fastidio vedere troppo codice html dentro al mio programma python, 
    quindi ho deciso di separarlo
"""


def head_html() -> str:
    """
        Ho creato questa funzione per poi chiamarla all'interno 
        del main perchè vedere la stringa multiline nel main e orribile
    """
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>schtasks</title>
            <meta charset='utf-8'>
            <meta name='viewport' content='width=device, initiale-scale=1.0'>
            <meta author='Bastianello Federico'>
        </head>
        <body>
    """


def end_html() -> str:
    """
        Ho creato questa funzione per poi chiamarla all'interno 
        del main perchè vedere la stringa multiline nel main e orribile
    """
    return """
        </body>
    </html>
    """


def insert_into_tdtag(fhtml: object, row_splitted: list):
    """
        Inserisco nel corpo del tbody row_splitted. Ogni elemento è separato da <td> e </td>
        Non serve restituire il file perchè alla chiamata si passa il fd
    """
    fhtml.write("<tr>\n")
    for element in row_splitted:
        fhtml.write("<td>" + str(element) + "</td>\n")
    fhtml.write("</tr>\n")


def insert_into_thtag(fhtml: object, inestazione: list):
    fhtml.write("<tr>\n")
    for element in inestazione:
        fhtml.write("<th>" + str(element) + "</th>\n")
    fhtml.write("</tr>\n")
