#echo "[distutils] 
#index-servers=pypi
#[pypi] 
#repository = https://upload.pypi.org/legacy/ 
#username =javatechy" > ~/.pypirc
#python -m kmisc upload dist/*

#or 
# python setup.py register # register account
# python setup.py sdist upload

# Test upload
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m twine upload --repository testpypi dist/*

# Real upload
#twine upload dist/*
