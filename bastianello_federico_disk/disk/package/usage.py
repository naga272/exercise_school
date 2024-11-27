
from ansic import *
import ansic


import wmi


def main():
    disks = wmi.WMI().Win32_LogicalDisk()
    for disk in disks:
        printf(f"dimensione del disco {disk.Name} {int(disk.FreeSpace) // (1024 ** 3)}")

    return EXIT_SUCCESS


if __name__ == "__main__":
    if ansic.log("../log/trace.csv", ansic.__FILE__) == EXIT_SUCCESS:
        if main() == EXIT_SUCCESS:
            printf(f"uscita dal programma con valore: {EXIT_SUCCESS}")
            ansic._exit(EXIT_SUCCESS)
    else:
        printf(f"errore nella creazione del log! uscita dal programma con valore: {EXIT_FAILURE}")

    ansic._exit(EXIT_FAILURE)