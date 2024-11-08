RegList<br>
<br>
Outputs a requirements.txt file based on the source files. <br>
<br>
Reason:<br>
Freeze will dump the entire list of installed packages<br>
pip3 freeze > requirements.txt<br>
<br>
Pipregs was throwing errors<br>
pipreqs -h<br>
ModuleNotFoundError: No module named 'urllib3.packages.six.moves'<br>
<br>
Wanted a pure python implimentation that I could customize for my projects<br>

<br>
Usage:<br>
python3 main.py [source] -r -a<br>
<br>
Arguments:<br>
source: the source folder to scan<br>
-r: Scans the source in recursive mode<br>
-a: Scans all files not just .py files<br>
<br>
Outputs:<br>
Creates a file names 'requirments.txt' in the source directory in the following format.<br>
aiofiles==23.2.1<br>
aiohttp==3.9.1<br>
pytz==2022.7<br>
setuptools==69.0.3<br>

