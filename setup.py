#Kage Park
import os
import setuptools
from sys import version_info
import subprocess

# require package
#python -m pip install wheel --user
#python -m pip install --upgrade build --user

def lib_ver():
    gver=subprocess.check_output('''git describe --tags >/dev/null && (git describe --tags | sed "s/^v//g" | sed "s/^V//g") || (git tag V1.0; sleep 1; git describe --tags | sed "s/^v//g" | sed "s/^V//g")''',stderr=subprocess.STDOUT,shell=True)
    if gver:
        if version_info[0] >= 3 and isinstance(gver,bytes):
            return '.'.join(gver.decode('latin1').split('\n')[0].split('-')[:-1])
        elif isinstance(gver,unicode):
            return '.'.join(gver.encode('latin1').split('\n')[0].split('-')[:-1])
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
    autor_email='kagepark1@gmail.com',
    license="MIT",
    description='Enginering useful function',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kagepark/kmisc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
#    install_requires=["feedparser", "html2text"],
)
