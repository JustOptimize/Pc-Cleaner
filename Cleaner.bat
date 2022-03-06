@echo off
Title Cleaner (v3)
C:
cd C:\Windows\System32\
net stop "SysMain" 
net stop "EventLog"
net stop "seclogon"
net stop "CryptSvc"

echo Services Done!

REG delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU" /va /f >nul
REG delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths" /va /f >nul
REG delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU" /va /f >nul
REG delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU" /va /f >nul
REG delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Internet Explorer\TypedURLs" /va /f >nul
REG delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Internet Explorer\TypedURLsTime" /va /f >nul
REG delete "HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store" /va /f >nul

echo Reg Done!

FSUTIL USN DELETEJOURNAL /D C: >nul && echo Cleaning C:\ Journal
IF EXIST "D:\" FSUTIL USN DELETEJOURNAL /D D:  >nul && echo Cleaning D:\ Journal
IF EXIST "F:\" FSUTIL USN DELETEJOURNAL /D F:  >nul && echo Cleaning F:\ Journal

echo Journal Done!

::Custom files
::del /F /Q %APPDATA%\Notepad++\session.xml >nul
::del /F /Q %APPDATA%\notepad++\config.xml >nul

echo Custom Files Done!

D:
cd "D:\Program Files\CCleaner"
CCleaner64.exe
echo CCleaner Done!

F:
cd "F:\z.2 Stuff\0. FPS BOOST PACK\1 Mirko303\RegSeeker"
RegSeeker.exe

echo RegSeeker Done!


netsh winsock reset >nul
ipconfig /renew >nul
ipconfig /flushdns >nul
ipconfig /release >nul
echo Network Done!

::Event viewer logs

::for /F "tokens=*" %%G in ('wevtutil.exe el') DO (call wevtutil.exe cl "%%G")
::wmic nteventlog where filename='security' cleareventlog >nul
::wmic nteventlog where filename='system' cleareventlog >nul

echo.
echo Press any key 3 times to restart your pc
pause >nul
pause >nul
pause >nul
shutdown /r /c "Optimization" /t 3