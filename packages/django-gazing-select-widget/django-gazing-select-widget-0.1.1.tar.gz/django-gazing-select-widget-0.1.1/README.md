# django-gazing-select-widget

Choices of select widget changes while the value of another filed changes.

## Install

```shell
pip install django-gazing-select-widget
```

## DjangoGazingSelectWidget Init Parameters

```python

class DjangoGazingSelectWidget(Select):

    def __init__(self,
            gazing_field_name,
            this_field_name,
            choices_related=None,
            gazing_related=True,
            optgroups_related=None,
            empty_label="-"*10,
            hide_all_if_empty=True,
            attrs=None,
            choices=(),
            ):
        ...
```

- gazing_field_name: Name of the gazing field.
- this_field_name: Name of this field.
- choices_related: List of tuple (option_value, related_value)
    - It means, if the gazing_field value equals to related_value, then the option with option_value will be show.
- gazing_related: Default to true, means gazing field is at the same level with this field.
    - If set to false, then the gazing field is always at the top level of the form.
- empty_label: Defualt to "-"*10. Empty value option for this field. 
- hide_all_if_empty: Default to true. If true, hide all options if gazing value is empty. If false, show all options if gazing value is empty.
- attrs: Same with system's default Select widget.
- choices: Same with system's default Select widget.
    - choices can be a callable object, if it's a callable object, it will be called again before get_context.

## Usage

**pro/settings.py

```python
INSTALLED_APPS = [
    ...
    'django_static_jquery3',
    'django_gazing_select_widget',
    ...
]
```

**app/admin.py**

```python
from django.contrib import admin
from django import forms
from django_gazing_select_widget.widgets import DjangoGazingSelectWidget
from .models import Category

cat1_choices = [
    ("", "-"*10),
    (1, "1"),
    (2, "2"),
]

cat2_choices = [
    ("group1", [
        (1, "a1"),
        (2, "b1"),
        (3, "c1"),
        (4, "d1"),
    ]),
    ("group2", [
        (5, "a2"),
        (6, "b2"),
        (7, "c2"),
        (8, "d2"),
    ]),
]

cat2_choices_related = {
    1: ["1"],
    2: ["1"],
    3: ["1"],
    4: ["1"],
    5: ["2"],
    6: ["2"],
    7: ["2"],
    8: ["2"],
}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        widgets = {
            "cat1": forms.Select(choices=cat1_choices),
            "cat2": DjangoGazingSelectWidget(gazing_field="cat1", choices=cat2_choices, choices_related=cat2_choices_related, hide_all_if_empty=False),
        }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["cat1", "cat2", "name"]
    form = CategoryForm

admin.site.register(Category, CategoryAdmin)

```

**Note:**

1. field cat2 is gazing at field cat1.
1. if the field cat1's value is empty, show none options in field cat2.
1. if the field cat1's value is 1, show group1 options in field cat2.
1. if the field cat1's value is 2, show group2 options in field cat2.


## Releases

### v0.1.1 2020/03/28

- Add callable choices support.
- Add gazing_related support.

### v0.1.0 2020/03/28

- First release.