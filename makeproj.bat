ren C:\Users\Public\Downloads\dist\Base\wordbase.json wordbase.mock
ren C:\Users\Public\Downloads\dist\Base\_wordbase.json wordbase.json
pyinstaller --noconfirm --add-data="myproj.ini;." myproj.py
pyinstaller --noconfirm fillbase.py
xcopy /e /y dist C:\Users\Public\Downloads\dist
