RegList

Outputs a requirements.txt file based on the source files. 

Reason:
Freeze will dump the entire list of installed packages
pip3 freeze > requirements.txt

Pipregs was throwing errors
pipreqs -h
ModuleNotFoundError: No module named 'urllib3.packages.six.moves'

Wanted a pure python implimentation that I could customize for my projects


Usage:
python3 reglist/app/main.py [source] -r -a

Arguments:
source: the source folder to scan
-r: Scans the source in recursive mode
-a: Scans all files not just .py files

Outputs:
Creates a file names 'requirments.txt' in the source directory in the following format.
aiofiles==23.2.1
aiohttp==3.9.1
pytz==2022.7
setuptools==69.0.3

