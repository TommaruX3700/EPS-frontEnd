!include "MUI.nsh"

; Script di installazione EPS per nsis

Name "EPS_Installer"
OutFile "EPS_Installer.exe"

InstallDir "$PROGRAMFILES\EPS"


; Pages

Page Directory
Page InstFiles

; Sections
Section
    SetOutPath $INSTDIR\Bootstrap
    File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\Bootstrap\bootstrap-5.0.2-dist\css\*"
    File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\Bootstrap\bootstrap-5.0.2-dist\js\*"

    SetOutPath $INSTDIR\wkhtmltox
    File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\wkhtmltox\*"

    SetOutPath $INSTDIR\EPS_MODEL
    File /r "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\EPS_MODEL\*"
    
    SetOutPath $INSTDIR
    File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\*"

    SetOutPath $INSTDIR\_internal
    File /r "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\*"

    ;SetOutPath $INSTDIR\_internal\fitz
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\fitz\*"
;
    ;SetOutPath $INSTDIR\_internal\markupsafe
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\markupsafe\*"
;
    ;SetOutPath $INSTDIR\_internal\numpy
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\numpy\*"
;
    ;SetOutPath $INSTDIR\_internal\numpy.libs
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\numpy.libs\*"
;
    ;SetOutPath $INSTDIR\_internal\pandas
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\pandas\*"
;
    ;SetOutPath $INSTDIR\_internal\pandas.libs
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\pandas.libs\*"
;
    ;SetOutPath $INSTDIR\_internal\PyQt5
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\PyQt5\*"
;
    ;SetOutPath $INSTDIR\_internal\pytz
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\pytz\*"
;
    ;SetOutPath $INSTDIR\_internal\pywin32_system32
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\pywin32_system32\*"
;
    ;SetOutPath $INSTDIR\_internal\win32
    ;File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\_internal\win32\*"


    CreateShortCut "$DESKTOP\EPS.lnk" "$INSTDIR\dist\EasyPalletSolution\EasyPalletSolution.exe"
SectionEnd

; Uninstaller

Section Uninstall
    Delete $INSTDIR\*
    RMDir $INSTDIR
    Delete "$SMPROGRAMS\EPS_Installer\*"
    RMDir "$SMPROGRAMS\EPS_Installer"
SectionEnd

;Function MakeMSI
;    ExecWait 'makensis.exe /V2 /DPRODUCT_NAME="EPS_Installer" /DPRODUCT_VERSION="1.0" /DMYAPPDIR="$INSTDIR" "EPS_Installer.nsi"'
;FunctionEnd
;
;; Call the function after installation
;!insertmacro MUI_PAGE_FINISH
;!insertmacro MUI_UNPAGE_FINISH
;Function .onInstSuccess
;    Call MakeMSI
;FunctionEnd
