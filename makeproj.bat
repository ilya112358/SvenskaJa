pyinstaller --noconfirm --add-data="myproj.ini;." myproj.py
pyinstaller --noconfirm fillbase.py
xcopy /e /y dist C:\Users\Public\Downloads\dist
