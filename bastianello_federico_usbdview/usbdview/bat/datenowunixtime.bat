@ECHO OFF
SETLOCAL
CALL :GetUnixTime UNIX_TIME
SET /A DT=%UNIX_TIME%
ECHO programma eseguito alle: %DT% >> ../log/trace_bat.txt
GOTO :EOF
:GetUnixTime
SETLOCAL enableextensions
FOR /f %%x IN ('wmic path wIN32_utctime get /FORmat:list ^| fINdstr "="') DO (
    SET %%x)
SET /a z=(14-100%Month%%%100)/12, y=10000%Year%%%10000-z
SET /a ut=y*365+y/4-y/100+y/400+(153*(100%Month%%%100+12*z-3)+2)/5+Day-719469
SET /a ut=ut*86400+100%Hour%%%100*3600+100%MINute%%%100*60+100%Second%%%100
ENDLOCAL & SET "%1=%ut%" & GOTO :EOF
:EOF
REM DT contiene il timestamp 
