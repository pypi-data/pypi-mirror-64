<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-site-local-middleware.svg?longCache=True)](https://pypi.org/project/django-site-local-middleware/)
[![](https://img.shields.io/pypi/v/django-site-local-middleware.svg?maxAge=3600)](https://pypi.org/project/django-site-local-middleware/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-site-local-middleware.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-site-local-middleware.py/)

#### Installation
```bash
$ [sudo] pip install django-site-local-middleware
```

#### Examples
`settings.py`

```python
DEBUG=True

MIDDLEWARE = [
    ...
    'django_site_local_middleware.middleware.SiteLocalMiddleware'
    ...
]
```

`/etc/hosts`
```
127.0.0.1   site.com.local
```


```bash
$ python manage.py runserver 0.0.0.0:8000
```

before|after
-|-
`<a href="http://site.com/">`|`<a href="http://site.com.local:8000/">`

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>