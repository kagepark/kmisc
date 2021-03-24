[ -d build ] && rm -fr build
[ -d dist ] && rm -fr dist
[ -d kmisc.egg-info ] && rm -fr kmisc.egg-info
#python3 setup.py bdist_wheel
python -m build
# Install
#python -m pip install dist/xxx.whl
