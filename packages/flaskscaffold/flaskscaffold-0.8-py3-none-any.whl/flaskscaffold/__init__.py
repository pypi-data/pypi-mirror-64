import os
from .create_scaffold import create_scaffold


def create():
    
    path = os.getcwd()
    print(f'Working directory: {path}')
    create_scaffold()
   

