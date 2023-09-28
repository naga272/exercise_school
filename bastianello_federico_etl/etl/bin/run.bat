@echo off
C:\Python311\python.exe sync.py ../flussi/77_gusers_export_alunni.csv ../flussi/77_SIGMA_EXPORT_ALUNNI.csv ../flussi/sync.csv
pause
create_gsuite.bat
deletegsuite.bat
pause
