# c (Windows)

Esta pasta é referente ao desenvolvimento no Ambiente Windows. Ainda está muito "crua" e tudo está tipo "atacado".

Powershell:

    Criar Ambiente Virtual:
        python ambiente.py python

    Activar Ambiente Virtual: 
        python/Scripts/Activate.ps1

    Iniciar o neoricalex:
        python neoricalex.py

    Pacote pip neoricalex:
        python -m pip install --upgrade setuptools wheel
        python setup.py sdist bdist_wheel

    Instalar Módulo para criar EXE:
        pip install --upgrade --no-cache-dir pyinstaller

    Criar EXE:
        pyinstaller --onefile -c neoricalex.py # Para esconder o terminal adicionar a flag -w

    UI:

        Transformar .ui em Python:
            pyuic5 -x <nome.ui> -o <nome.py>

Miscelaneous:

    Prompt de Comando:

        setups/python-3.8.2-amd64.exe
        python -m pip install --upgrade pip
        pip install --upgrade --no-cache-dir pyinstaller pysimplegui pyaudio gitpython
        cd c
        pyinstaller --onefile -w neoricalex.py
        cookiecutter https://github.com/neoricalex/cookiecutter-django.git

    Start-Process powershell -Verb runAs

    Powershell Administrador:

        Atualizar Windows 10:

            Install-Module PSWindowsUpdate
            Get-WindowsUpdate
            Install-WindowsUpdate

Ativar Sub-Sistema Linux:

    .\dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart 
    .\dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

Catálogo Windows:

    https://www.catalog.update.microsoft.com/