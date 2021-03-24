#Kage Park
import os
import setuptools
from sys import version_info
import subprocess

# require package: pip install wheel

def lib_ver():
    gver=subprocess.check_output('''git describe --tags >/dev/null && (git describe --tags | sed "s/^v//g" | sed "s/^V//g") || (git tag V1.0; sleep 1; git describe --tags | sed "s/^v//g" | sed "s/^V//g")''',stderr=subprocess.STDOUT,shell=True)
    if gver:
        if version_info[0] >= 3 and isinstance(gver,bytes):
            return gver.decode('latin1').split('\n')[0]
        elif isinstance(gver,unicode):
            return gver.encode('latin1').split('\n')[0]
    return '2.0'

long_description=''
if os.path.isfile('README.md'):
    with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name='kmisc',
    version='{}'.format(lib_ver()),
#    scripts=['klib'],
    author='Kage Park',
    #autor_email='',
    description='Enginering useful function',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kagepark/kmisc",
    packages=setuptools.find_packages(),
    classifiers=[
#        "Programming Language :: Python :: 2",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
)
