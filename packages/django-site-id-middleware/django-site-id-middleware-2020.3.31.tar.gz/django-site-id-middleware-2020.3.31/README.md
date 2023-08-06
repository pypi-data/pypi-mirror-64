<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-site-id-middleware.svg?longCache=True)](https://pypi.org/project/django-site-id-middleware/)
[![](https://img.shields.io/pypi/v/django-site-id-middleware.svg?maxAge=3600)](https://pypi.org/project/django-site-id-middleware/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-site-id-middleware.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-site-id-middleware.py/)

#### Installation
```bash
$ [sudo] pip install django-site-id-middleware
```

#### Cons
+   `django.contrib.syndication` not supported

#### Examples
`settings.py`

```python
MIDDLEWARE = [
    ...
    'django_site_id_middleware.middleware.SiteIdMiddleware'
    ...
]
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>