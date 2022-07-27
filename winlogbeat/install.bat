cd %1
powershell -command "PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-winlogbeat.ps1"
powershell -command ".\install-service-winlogbeat.ps1"
winlogbeat.exe test config -c .\winlogbeat.yml -e
