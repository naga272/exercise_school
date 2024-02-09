@echo off


echo il programma per sistema operativo linux richiede il compilatore nasm e il linker ld
sudo apt install nasm
echo
pip install pandas
pip install cython
pip install lxml

python3 ../bin/main.py ../flussi/movies_metadata.csv ../flussi/movies_metadata.xml ../flussi/movies_metadata.json

