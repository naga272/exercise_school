@echo off
color 1c

call datenowunixtime.bat
echo datenowunixtime.bat eseguito

cd ../bin/

USBDview.exe /stab ../flussi/usbdviewall.csv
echo programma USBDview eseguito
echo.

python usbdview.py ../flussi/usbdviewall.csv
echo programma python eseguito
echo.

move ..\flussi\*usbdviewnohid.csv c:\work\repousb\
echo file csv spostati in c:\work\repousb\

echo.
python sync.py c:\work\repousb\
echo file sync.py eseguito
echo.

pause