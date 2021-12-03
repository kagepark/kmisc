#echo "[distutils] 
#index-servers=pypi
#[pypi] 
#repository = https://upload.pypi.org/legacy/ 
#username =javatechy" > ~/.pypirc
#python -m kmisc upload dist/*

# Test upload
python3 -m twine upload --repository testpypi dist/*

# Real upload
#python3 -m twine upload --repository-url https://test.pypi.org/legacy/ --repository legacy dist/*
