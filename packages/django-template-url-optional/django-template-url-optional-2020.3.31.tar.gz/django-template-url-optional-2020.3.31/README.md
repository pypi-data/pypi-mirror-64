<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-template-url-optional.svg?longCache=True)](https://pypi.org/project/django-template-url-optional/)
[![](https://img.shields.io/pypi/v/django-template-url-optional.svg?maxAge=3600)](https://pypi.org/project/django-template-url-optional/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-template-url-optional.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-template-url-optional.py/)

#### Installation
```bash
$ [sudo] pip install django-template-url-optional
```

#### Examples
```html
{% load url_optional %}

<a href="{% url_optional 'item_list' variable %}">
<a href="{% url_optional 'item_list' %}">
```

`urls.py`
```python
urlpatterns = [
    path('<str:name>/', views.ItemListView.as_view(),name='item_list'),
    path('', views.ItemListView.as_view(),name='item_list'),
]
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>