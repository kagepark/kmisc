echo "[distutils] 
index-servers=pypi
[pypi] 
repository = https://upload.pypi.org/legacy/ 
username =javatechy" > ~/.pypirc
python -m twine upload dist/*

#or 
# python setup.py register # register account
# python setup.py sdist upload
