Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d C:\Users\dilla\OneDrive\Desktop\PyCodeBite && python -m streamlit run clean_nairobi_app.py --server.port 8501 --server.headless true", 0, False
Wscript.Sleep 3000
WshShell.Run """C:\Users\dilla\OneDrive\Desktop\PyCodeBite\PyCodeBite-win32-x64\PyCodeBite.exe""", 1, False