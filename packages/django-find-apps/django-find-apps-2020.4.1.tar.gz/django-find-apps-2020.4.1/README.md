<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-find-apps.svg?longCache=True)](https://pypi.org/project/django-find-apps/)
[![](https://img.shields.io/pypi/v/django-find-apps.svg?maxAge=3600)](https://pypi.org/project/django-find-apps/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-find-apps.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-find-apps.py/)

#### Installation
```bash
$ [sudo] pip install django-find-apps
```

#### Functions
function|`__doc__`
-|-
`django_find_apps.find_apps(path)` |return a list of apps

#### Examples
`settings.py`
```python
import django_find_apps

INSTALLED_APPS = django_find_apps.find_apps("apps")
```

```
apps
├── app1
|   ├── __init__.py
|   └── models.py
├── app2
|   ├── __init__.py
|   └── templatetags
└── app3
    ├── __init__.py
    └── management
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>