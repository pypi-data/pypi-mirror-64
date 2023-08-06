import os
import sys
import shutil  
import inspect

folders = ['models', 'controllers', 'services', 'tests', 'templates', 'static']

def create_scaffold():

    create_other_files()

    for folder in folders:
        try:
            os.mkdir(folder)
            create_init_file(folder)
        except OSError:
            print(f'Could not create subdirectory: {folder}')
        else:
            print(f'Created subdirectory: {folder}')


def create_init_file(foldername):
    
    project_dir = os.getcwd()

    if foldername in ['models', 'controllers', 'services']:
        try:
            os.chdir(os.path.join(os.getcwd(), foldername))
            open('__init__.py', 'w+')
            os.chdir(project_dir)
        except OSError:
            print(f'Could not create __init__.py for: {foldername}')
        else:
            print(f'Created __init__.py for: {foldername}')
    
    return


def create_other_files():  
    
    open('db.py', 'w+')
    
    pkgdir = sys.modules['flaskscaffold'].__path__[0]
    pkgsubdir = 'complimentary_files'
    fullpath = os.path.join(pkgdir, pkgsubdir, 'app.py')
    shutil.copy(fullpath, os.getcwd())

    fullpath = os.path.join(pkgdir, pkgsubdir, '.gitignore')
    shutil.copy(fullpath, os.getcwd())
    


