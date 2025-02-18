from setuptools import setup,find_packages
from typing import List
HYPHEN_E_DOT = "-e ."
def get_requirements(file_path: str) -> List[str]:
    """This function returns a list of requirements"""
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements
setup(
    name='mlproject',
    version='1.0.0',
    description='My Python package',
    author='Sumedha',
    author_email='sumedha3396@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')    
)