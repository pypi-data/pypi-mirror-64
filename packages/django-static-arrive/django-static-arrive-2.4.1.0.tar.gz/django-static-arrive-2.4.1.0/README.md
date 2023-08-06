# django-static-arrive

Django application contain arrive js files. And arrive js is absorbed in watching for DOM elements creation and removal.

## Install

```shell
pip install django-static-arrive
```

## Usage


**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    "django_static_jquery3",
    "django_static_arrive",
    ...
]
```

**app/templates/demo.html**


```
{% load static %}

<script src="{% static "jquery3/jquery.js" %}"></script>
<script src="{% static "arrive/arrive.min.js" %}"></script>
```

## Note

- Depends on jquery3.
- All js files are from https://github.com/uzairfarooq/arrive.
- The first third release numbers are js's release version numbers.
- The fourth release number is our release number.

## Releases

### v2.4.1.0

- First release.