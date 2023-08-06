import os
import sys
import shutil  
import inspect
import click
import pkg_resources

folders = ['models', 'controllers', 'services', 'tests', 'templates', 'static']


VERSION = pkg_resources.require("flaskscaffold")[0].version

@click.group()
@click.version_option(version=VERSION, prog_name='dokr')
def flaskscaffold():  # pragma: no cover
    pass


@click.command()
@click.option('--web', default=False, is_flag=True, help='Create bootstrap with templates and static folders')
def create_scaffold(web):

    path = os.getcwd()
    print(f'Working directory: {path}')
    print(web)
    create_other_files()
    if web:
        for folder in folders:
            try:
                os.mkdir(folder)
                create_init_file(folder)
            except OSError:
                print(f'Could not create subdirectory: {folder}')
            else:
                print(f'Created subdirectory: {folder}')
    else:
        for folder in folders:
            if folder in ['templates','static']:
                continue
            else:
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
    


flaskscaffold.add_command(create_scaffold)


if __name__ == '__main__':  # pragma: no cover
    flaskscaffold()