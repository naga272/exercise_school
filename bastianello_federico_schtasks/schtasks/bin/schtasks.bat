@echo off

schtasks.exe /query /fo csv /v > ../flussi/tasks.csv
python.exe schtasks.py ../flussi/tasks.csv ../flussi/tasks_filter.csv