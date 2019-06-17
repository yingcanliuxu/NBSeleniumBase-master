## ![http://seleniumbase.com](https://cdn2.hubspot.net/hubfs/100006/images/super_logo_tiny.png "SeleniumBase") SeleniumBase Installation

If you're installing SeleniumBase from a cloned copy on your machine, use:
```
pip install -U -r requirements.txt

python setup.py install
```

If you're installing SeleniumBase directly [from PyPI (the Python Package Index)](https://pypi.python.org/pypi/seleniumbase), use:
```bash
pip install -U seleniumbase
```

If you're installing SeleniumBase directly [from GitHub](https://github.com/seleniumbase/SeleniumBase), use:
```bash
pip install -U -e git+https://github.com/seleniumbase/SeleniumBase.git@master#egg=seleniumbase
```

(If you're not using a virtual environment, you may need to add ``--user`` to your ``pip`` command if you're getting errors during installation.)
