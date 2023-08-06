import json
from django.forms.widgets import Select

class DjangoGazingSelectWidget(Select):

    class Media:
        js = [
            "jquery3/jquery.js",
            "django-gazing-select-widget/js/django-gazing-select-widget.js",
        ]


    def __init__(self, gazing_field_name, this_field_name, choices_related=None, optgroups_related=None, empty_label="-"*10, hide_all_if_empty=True, attrs=None, choices=()):
        # keep private parameters
        self.choices_related = choices_related or {}
        self.optgroups_related = optgroups_related or {}
        # super.init
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " django-gazing-select-widget"
        attrs["data-gazing-field-name"] = gazing_field_name
        attrs["data-this-field-name"] = this_field_name
        attrs["data-hide-all-if-empty"] = hide_all_if_empty and "true" or "false";
        choices.insert(0, ("", empty_label))
        super().__init__(attrs, choices)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        for optgroup in context["widget"]["optgroups"]:
            group_title = optgroup[0]
            optgroup_for = self.optgroups_related.get(group_title, [])
            for option in optgroup[1]:
                option_value = option["value"]
                option_for = [] + optgroup_for
                if self.choices_related:
                    option_for += self.choices_related.get(option_value, [])
                option["attrs"]["data-for"] = json.dumps(option_for)
        return context
