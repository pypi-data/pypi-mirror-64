import os
from cli.utils import created_by


def create_init(folder):
    """Creates an __init__.py file into folder"""
    if os.path.isfile(folder):
        folder = os.path.dirname(folder)

    init_file = os.path.join(folder, '__init__.py')
    if not os.path.isfile(init_file):
        with open(init_file, 'w') as f:
            f.write(created_by()+"\n")
    folder = os.path.dirname(folder)
