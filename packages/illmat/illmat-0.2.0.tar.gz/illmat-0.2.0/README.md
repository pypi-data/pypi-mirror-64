# deprecated package



```
python3.6 -m venv .venv
source .venv/bin/activate
pip install twine
python setup.py sdist && twine upload -r pypi dist/*
```
