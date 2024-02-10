

from    module.converter import main
import  subprocess
import  sys
import  os


def verifica_PATH(y):
    '''
        *
        *   Funzione che mi consente di verificare se un programma si trova nella PATH
        *
    '''
    try:
        subprocess.run([y, '--version'], 
                       stdout = subprocess.PIPE, 
                       stderr = subprocess.PIPE, 
                       check = True)
        return 1
    except subprocess.CalledProcessError:
        return 0


if __name__ == "__main__":
    result = 1

    if 0 in [verifica_PATH("nasm"), verifica_PATH("ld")]:
        print("errore! compilatore nasm e ld non si trovano nella PATH")
    else:
        result = main(len(sys.argv), sys.argv, [(key,value) for key, value in os.environ.items()])

    print("stato di uscita dal programma: ", result)
    sys.exit(result)

