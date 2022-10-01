cd %1
powershell -command "Get-EventLog *"
powershell -command "Start-Service winlogbeat"
