@echo off
setlocal enabledelayedexpansion

set "repo_root=%cd%"
if not "%repo_root:~-1%"=="\" set "repo_root=%repo_root%\"

if "%~1"=="" (
    set "TARGET_DIR=."
) else (
    set "TARGET_DIR=%~1"
)

if not exist "%TARGET_DIR%" (
    echo The specified directory "%TARGET_DIR%" does not exist.
    exit /b 1
)

echo Processing files in "%TARGET_DIR%"

for /R "%TARGET_DIR%" %%F in (*) do (
    set "absFile=%%F"
    set "relFile=!absFile:%repo_root%=!"

    git ls-files --error-unmatch "!relFile!" >nul 2>&1
    if errorlevel 1 (
        echo Skipping untracked file "!relFile!"
    ) else (
        set "fname=%%~nF"
        set "ext=%%~xF"

        if not "!fname!"=="" (
            set "firstLetter=!fname:~0,1!"
            set "firstLetterUpper=!firstLetter!"
            set "firstLetterUpper=!firstLetterUpper:a=A!"
            set "firstLetterUpper=!firstLetterUpper:b=B!"
            set "firstLetterUpper=!firstLetterUpper:c=C!"
            set "firstLetterUpper=!firstLetterUpper:d=D!"
            set "firstLetterUpper=!firstLetterUpper:e=E!"
            set "firstLetterUpper=!firstLetterUpper:f=F!"
            set "firstLetterUpper=!firstLetterUpper:g=G!"
            set "firstLetterUpper=!firstLetterUpper:h=H!"
            set "firstLetterUpper=!firstLetterUpper:i=I!"
            set "firstLetterUpper=!firstLetterUpper:j=J!"
            set "firstLetterUpper=!firstLetterUpper:k=K!"
            set "firstLetterUpper=!firstLetterUpper:l=L!"
            set "firstLetterUpper=!firstLetterUpper:m=M!"
            set "firstLetterUpper=!firstLetterUpper:n=N!"
            set "firstLetterUpper=!firstLetterUpper:o=O!"
            set "firstLetterUpper=!firstLetterUpper:p=P!"
            set "firstLetterUpper=!firstLetterUpper:q=Q!"
            set "firstLetterUpper=!firstLetterUpper:r=R!"
            set "firstLetterUpper=!firstLetterUpper:s=S!"
            set "firstLetterUpper=!firstLetterUpper:t=T!"
            set "firstLetterUpper=!firstLetterUpper:u=U!"
            set "firstLetterUpper=!firstLetterUpper:v=V!"
            set "firstLetterUpper=!firstLetterUpper:w=W!"
            set "firstLetterUpper=!firstLetterUpper:x=X!"
            set "firstLetterUpper=!firstLetterUpper:y=Y!"
            set "firstLetterUpper=!firstLetterUpper:z=Z!"

            if "!firstLetter!"=="!firstLetterUpper!" (
                echo Skipping "!relFile!", already capitalized.
            ) else (
                set "newName=!firstLetterUpper!!fname:~1!!ext!"
                for %%I in ("!relFile!") do set "relDir=%%~dpI"
                set "newRelFile=!relDir!!newName!"
                set "tempName=temp_%%~nxF"
                set "tempRelFile=!relDir!!tempName!"

                echo Renaming "!relFile!" to "!newRelFile!"
                git mv "!relFile!" "!tempRelFile!"
                git mv "!tempRelFile!" "!newRelFile!"
            )
        )
    )
)

endlocal
