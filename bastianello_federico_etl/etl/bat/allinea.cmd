@echo off
python.exe ../bin/sync.py ../flussi/77_gusers_export_alunni.csv ../flussi/77_SIGMA_EXPORT_ALUNNI.csv ../flussi/sync.csv %1%
if "%1%" == "prima" (
	call mov.bat
)
if "%1%" == "dopo" (
	call creategsuite.bat
	call deletegsuite.bat
)
pause
