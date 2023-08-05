from setuptools import setup
import os



def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        print(dirs)
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, '', 1)
            stubs.append(path)
    return {package: stubs}

# twine upload --skip-existing --repository pypi dist/*
setup(
    name='ortools-stubs',
    maintainer="Xiang Chen",
    maintainer_email="xiangchenchen96@gmail.com",
    description="PEP 561 type stubs for Google OR-Tools",
    url="https://github.com/stradivari96/ortools-stubs",
    license='MIT',
    version="7.5",
    packages=['ortools-stubs'],
    package_data=find_stubs('ortools-stubs'),
)
