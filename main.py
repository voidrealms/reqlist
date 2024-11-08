import logging
import sys
import os
import subprocess

def get_confirmation(prompt:str) -> bool:
    """Asks the user for confirmation
    
    Arguments:
        prompt (str): The text prompt
    """ 
    value = input('{prompt} (Y / N):'.format(prompt=prompt)).strip().upper()
    if(value == 'Y'):
        return True
    return False


def get_path() -> str:
    """Returns the path to scan"""
    srcpath = ''
    logging.debug('Args: {args}'.format(args=sys.argv))
    if(len(sys.argv) < 2):
        logging.debug('No command line args')
        print('Opps looks like you forgot the source path argument.')
        srcpath = input('Enter a directory:')
    else:
        logging.debug('Use command line args')
        srcpath = sys.argv[1]
    
    if(not os.path.exists(srcpath)):
        print('The source path was not found!')
        return get_path()
    return srcpath

def get_files(source:str,recursive:bool) -> list:
    """Gets the files in a folder
    
    Arguments:
        source (str): The source path
        recursive (bool): Determines if the sub folders are scanned

    Returns:
        list: List of files
    """
    logging.debug('Getting files from:{source}, recursive: {recursive}'.format(source=source,recursive=recursive))
    items = list()
    if(not recursive):
        logging.debug('Scanning single')
        for item in os.listdir(source):
            path = os.path.join(source,item)
            if(os.path.isfile(path)):
                found = os.path.join(source,item)
                if(found not in items):
                    items.append(found)
    else:
        logging.debug('Scanning recursive')
        for root, dirs, files in os.walk(source):
            for file in files:
                found = os.path.abspath(os.path.join(root,file))
                if(found not in items):
                    items.append(found)
    return items

def get_imports(filepath:str) -> list:
    """Reads a file and returns the imports
    
    Arguments:
        filepath (str): The file path
    
    Returns:
        list: List of imports
    """
    items = list()
    with open(filepath,'r') as f:
        for line in f.readlines():
            if(line.startswith('import ') or line.startswith('from ')):
                parts = line.split(' ')
                part = parts[1].strip()
                if('.' in part):
                    items.append(part.split('.')[0])
                else:
                    items.append(part)
    return items

def get_installed() -> list:
    """Returns a list of installed packages"""
    cmd = 'pip3 list'
    result = subprocess.run(['pip3', 'list'], stdout=subprocess.PIPE)
    installed = list()
    
    for part in result.stdout.splitlines():
        line = part.decode("utf-8")
        parts =line.split(' ')
        installed.append('{package}=={version}'.format(package=parts[0],version=parts[-1]))
    return installed

def scan(source:str) -> list:
    """Scans the source path and gets a list of imports
    
    Arguments:
        source (str): The source path to scan
    """
    print('Source path: {source}'.format(source=source))
    recursive = False
    allfiles = False

    if('-r' in sys.argv):
        recursive = True

    if('-a' in sys.argv):
        allfiles = True

    if(len(sys.argv) < 2):
        recursive = get_confirmation('Scan all directories?')
        allfiles = get_confirmation('Scan all files?')

    files = get_files(source,recursive)
    imports = list()
    for file in files:
        if(not allfiles and not file.upper().endswith('.PY')):
            logging.debug('Skipping {file}'.format(file=file))
            continue
        for item in get_imports(file):
            if(item not in imports):
                logging.debug('Adding {file}'.format(file=file))
                imports.append(item)
    return imports

def get_required(imports:list,installed:list) -> list:
    """Gets the required items from the list of installed items
    
    Arguments:
        imports (list): The list of imported packages from the scanned files
        installed (list): The list of installed packages
    
    Returns:
        list: The final list of required packages
    """
    required = list()
    for installed_item in installed:
        name = installed_item.split('==')[0]
        if(name in imports):
            required.append(installed_item)
    logging.debug('Requried: {required}'.format(required=required))
    return required

def save_file(required:list,destination:str):
    if(len(required) == 0):
        print('No required packages found!')
        return
    filename = 'requirements.txt'
    filepath = os.path.join(destination,filename)
    if(os.path.exists(filepath)):
        print('WARNING - the file {filename} already exists!'.format(filename=filename))
        confirm = get_confirmation('Overwrite {filename}?'.format(filename=filename))
        if(not confirm):
            print('Exiting with out saving {filename}!'.format(filename=filename))
            return
    print('Saving {filename}!'.format(filename=filename))
    with open(filepath,'w') as f:
        f.write('\n'.join(required))
    print('Done!')

def main():
    source_path = get_path()
    imports = scan(source_path)
    installed = get_installed()
    required = get_required(imports,installed)
    save_file(required,source_path)
    
if(__name__ == '__main__'):
    logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',datefmt='%H:%M:%S', level=logging.INFO)
    main()
