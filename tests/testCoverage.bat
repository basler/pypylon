del /F /S htmlcov
del .coverage
del pylon\gigE\.coverage
del pylon\emulated\.coverage
del pylon\usb\.coverage
del ..\samples\.coverage

for %%f in (genicam\*test.py) do (
	"C:\Program Files\Python35\Scripts\coverage.exe" run -a -L --source=pypylon --branch %%f
    )
cd pylon\emulated\
for %%f in (*test.py) do (
	"C:\Program Files\Python35\Scripts\coverage.exe" run -a -L --source=pypylon --branch -m unittest %%f
    )
cd ..\gigE\
for %%f in (*test.py) do (
	"C:\Program Files\Python35\Scripts\coverage.exe" run -a -L --source=pypylon --branch -m unittest %%f
    )
cd ..\usb\
for %%f in (pylon\usb\*test.py) do (
	"C:\Program Files\Python35\Scripts\coverage.exe" run -a -L --source=pypylon --branch -m unittest %%f
    )
cd ..\..\..\samples
for %%f in (*.py) do (
	"C:\Program Files\Python35\Scripts\coverage.exe" run -a -L --source=pypylon --branch %%f
    )
cd ..\tests\
"C:\Program Files\Python35\Scripts\coverage.exe" combine -a .coverage pylon\gigE\.coverage
"C:\Program Files\Python35\Scripts\coverage.exe" combine -a .coverage pylon\usb\.coverage
"C:\Program Files\Python35\Scripts\coverage.exe" combine -a .coverage pylon\emulated\.coverage
"C:\Program Files\Python35\Scripts\coverage.exe" combine -a .coverage ..\samples\.coverage
"C:\Program Files\Python35\Scripts\coverage.exe" html
pause