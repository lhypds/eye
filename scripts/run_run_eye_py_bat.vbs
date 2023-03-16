Set WshShell = CreateObject("WScript.Shell" )
WshShell.Run "taskkill /im python.exe /f", , True
WScript.Sleep 5000
WshShell.Run """C:\code\github-gcc\eye\run_eye_py.bat""", 0, True 'Must quote command if it has spaces; must escape quotes
Set WshShell = Nothing
