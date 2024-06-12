!include "MUI.nsh"

; Script di installazione EPS per nsis

BGGradient 800080 000000 FFFFFF
Name "EPS_Installer"
OutFile "EPS_Installer.exe"

InstallDir "$APPDATA\EPS"


; Pages

Page Directory
Page InstFiles

; Sections
Section
    SetOutPath $INSTDIR\Bootstrap
    File /r "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\Bootstrap\*"
    File /r "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\Bootstrap\*"

    SetOutPath $INSTDIR\wkhtmltox
    File /r "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\wkhtmltox\*"

    SetOutPath $INSTDIR\EPS_MODEL
    File /r "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\EPS_MODEL\*"

    SetOutPath $INSTDIR
    File "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\*"
    
    SetOutPath $INSTDIR
    File /r "C:\Users\aless\Documents\sviluppi\TEAMWORKING_29-4-24\EPS-frontEnd\stable\BUILD\dist\EasyPalletSolution\*"

    ;CreateShortCut "$INSTDIR\EasyPalletSolution.lnk" "$INSTDIR\dist\EasyPalletSolution\EasyPalletSolution.exe"
    
    WriteUninstaller $INSTDIR\EPS_Uninstaller.exe
SectionEnd

; Uninstaller

Section Uninstall
    SetOutPath $TEMP

    Delete "$INSTDIR\Bootstrap\*"
    RMDir /r "$INSTDIR\Bootstrap"
    Delete "$INSTDIR\wkhtmltox\*"
    RMDir /r "$INSTDIR\wkhtmltox"
    Delete "$INSTDIR\EPS_MODEL\*"
    RMDir /r "$INSTDIR\EPS_MODEL"
    
    Delete "$INSTDIR\*"
    RMDir "$INSTDIR"
SectionEnd


!finalize 'sign.bat "%1"' ; %1 inside the batch file is the .exe to sign
!uninstfinalize 'sign.bat "%1"'
