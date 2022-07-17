ren C:\Users\Public\Downloads\dist\Base\wordbase.json wordbase.mock
ren C:\Users\Public\Downloads\dist\Base\_wordbase.json wordbase.json
pyinstaller --noconfirm myproj.py 
pyinstaller --noconfirm fillbase.py 
xcopy /e /y dist C:\Users\Public\Downloads\dist