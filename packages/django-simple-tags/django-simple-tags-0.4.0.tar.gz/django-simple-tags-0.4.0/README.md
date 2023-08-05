# django-simple-tags

Collection of simple django tags and filters.

## Install

```shell
pip install django-simple-tags
```

## Installed Tags or Filters

- Tags
    - sprintf
    - string_format
    - admin_url
    - if_cookie
    - get_cookie
    - has_cookie
    - if_setting
    - get_setting
    - has_setting
    - model_select_include
    - call
    - call_method
- Filters
    - add_string_gap
    - add_string_left_gap
    - add_string_right_gap
    - get_model_verbose_name
    - get_model_app_label
    - get_model_name
    - get_model_fullname

## Settings

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_simple_tags',
    ...
]
```

## Usage

```django
{% load django_simple_tags %}

{% load django_simple_tags %}

<h1>{% sprintf "hello %s" "Tom" %}</h1>

<h1>{% string_format "hi {0}" "Tom" %}</h1>

<h1>{% string_format "hi {name}" name="Tom" %}</h1>

<h1>{% string_format "{0} + {1} = {result}" 3 4 result=7 %}</h1>

<a href="{% admin_url cat "change" %}">{% admin_url cat "change" %}</a>

<h1>{% if_cookie request "sessionid" "存在sessionid" "不存在sessionid" %}</h1>

<h1>{% get_cookie request "sessionid" %}</h1>

<h1>{% has_cookie request "sessionid" as has_sessionid %}{% if has_sessionid %}存在sessionid{% else %}不存在sessionid{% endif %}</h1>

<h1>{% if_cookie request "xsessionid" "存在xsessionid" "不存在xsessionid" %}</h1>

<h1>{% get_cookie request "xsessionid" "None" %}</h1>

<h1>{% has_cookie request "xsessionid" as has_xsessionid %}{% if has_xsessionid %}存在xsessionid{% else %}不存在xsessionid{% endif %}</h1>

<h1>{% if_setting "DEBUG" "存在DEBUG" "不存在DEBUG" %}</h1>

<h1>{% get_setting "DEBUG" %}</h1>

<h1>{% has_setting "DEBUG" as has_debug %}{% if has_debug %}存在DEBUG{% else %}不存在DEBUG{% endif %}</h1>

<h1>{% if_setting "NO_DEBUG" "存在NO_DEBUG" "不存在NO_DEBUG" %}</h1>

<h1>{% get_setting "NO_DEBUG" False %}</h1>

<h1>{% has_setting "NO_DEBUG" as has_no_debug %}{% if has_no_debug %}存在NO_DEBUG{% else %}不存在NO_DEBUG{% endif %}</h1>

{% model_select_include cat "hello.html" %}

{% model_select_include cat "world.html" %}

{% model_select_include cat "hi.html" %}

<h1>{% sprintf "Select%sto view" "Category"|add_string_gap:" " %}</h1>

<h1>{% sprintf "Select%sto view" "Category"|add_string_left_gap:" ["|add_string_right_gap:"] " %}</h1>

<h1>{{model_class|get_model_app_label}}</h1>

<h1>{{model_class|get_model_name}}</h1>

<h1>{{model_class|get_model_fullname}}</h1>

<h1>{{model_class|get_model_verbose_name}}</h1>


```

## Releases

### v0.4.0 2020/03/21

- Add tags: call, call_method

### v0.3.0 2020/03/03

- Add filters: get_model_app_label, get_model_name, get_model_fullname, get_model_verbose_name.

### v0.2.0 2020/02/23

- Fix document.
- Remove print statements.
- Add filters: add_string_gap, add_string_left_gap, add_string_right_gap.

### v0.1.0 2020/02/23

- First release.
