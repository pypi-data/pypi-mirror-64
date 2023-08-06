# xvgpy
A scriptable vector graphics library for Python

**Installing**
(See: https://pypi.org/project/xvg/)
```
python3 -m pip install xvg
```
**Testing** (See: https://docs.python.org/3/library/unittest.html)
```
python3 -m unittest
```
**Publishing** (See: https://packaging.python.org/tutorials/packaging-projects/)
```
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

python3 -m pip install --user --upgrade twine
python3 -m twine upload dist/*
```