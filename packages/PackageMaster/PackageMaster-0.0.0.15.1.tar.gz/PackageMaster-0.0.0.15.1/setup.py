#from distutils.core import setup
from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = 'PackageMaster',
    packages = ['PackageMaster'],
    version = '0.0.0.15.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Shaon Majumder',
    author_email = 'smazoomder@gmail.com',
    url = 'https://github.com/ShaonMajumder/PackageMaster',
    download_url = 'https://github.com/ShaonMajumder/PackageMaster/archive/0.0.0.15.1.tar.gz',
    keywords = ['Package Maker', 'PyPi Uploader', 'Shaon Majumder'],
    classifiers = [],
    setup_requires=['wheel'],
    entry_points={
        'console_scripts': [
            'PackageMaster=PackageMaster.PackageMaster:main',
        ],
    },
    package_data= {'': ['resources/*', '*']}
)