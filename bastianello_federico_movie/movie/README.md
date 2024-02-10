# movie
![Language](https://img.shields.io/badge/Spellcheck-Pass-green?style=flat)   ![Platform](https://img.shields.io/badge/OS%20platform%20supported-Linux-blue?style=flat) ![Platform](https://img.shields.io/badge/OS%20platform%20-Linux-blue?style=flat) ![Language](https://img.shields.io/badge/Language-Python-yellowgreen?style=flat) ![Language](https://img.shields.io/badge/Language-cython-yellowgreen?style=flat) ![Language](https://img.shields.io/badge/Language-asm-blue?style=flat) ![Testing](https://img.shields.io/badge/Test-Pass-green)

## description
Programma python che richiede tre argomenti:
- il primo argomento deve essere il percorso di dove è situato il file csv da convertire (N.B.: deve avere come separatori la ,)
- il secondo rappresenta il percorso dove verra creato il file xml.
- il terzo rappresenta il percorso dove verra creato il file json.

Il programma permette di convertire un file csv in un file xml e json.
Esperimento: far comunicare bash, python, cython e assembly usando sottoprocessi.  

## requirements
    - cpu x32 o x64
    - interprete python >= 3.10
    - compilatore nasm (aggiunto alla path)
    - linker ld (aggiunto a path)
    - o.s. Unix Like (il programma è stato testato solo su Linux)
    - librerie python non standard (vedere requirements.txt)

Per o.s. Windows:
Il compilatore nasm può essere scaricato sul sito [nasm.us](https://www.nasm.us), invece il linker ld può essere scaricato sul sito [GnuWin](https://gnuwin32.sourceforge.net/packages/ld.htm) (NB: sia ld che nasm devono essere inclusi nella PATH per far funzionare il programma).

Una volta scaricato nasm e ld bisogna andare nella directory /bin/ e scrivere il comando da cmd:
-	python setup.py build_ext --inplace
Tuttavia, non si garantisce la corretta esecuzione del programma, non potendo testarlo su Windows.

## execution
dipende dal sistema operativo:
    - Linux:    eseguire il programma /bat/run.sh
	- Windows:  eseguire il programma /bat/run.bat 

## tags
system os sys platform time datetime cython libc.stdlib json xml cimport exit void syscall int80h .data .text .bss _start _exit macro subprocess run PIPE try except

## author
Bastianello Federico
