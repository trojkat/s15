from typing import List

from django import forms

from themes.types import ThemeSetting


class ThemeSettingsForm(forms.Form):

    def __init__(self, settings: List[ThemeSetting], current_settings: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for setting in settings:
            if setting.type == "text":
                field = forms.CharField(
                    label=setting.name,
                    required=False,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    initial=setting.default,
                    help_text=setting.help_text,
                )
            if setting.type == "image":
                field = forms.ImageField(
                    label=setting.name,
                    required=False,
                    # widget=forms.TextInput(attrs={'class': 'form-control'}),
                    # initial=setting.default,
                    help_text=setting.help_text,
                )
            elif setting.type == "choice":
                field = forms.ChoiceField(
                    label=setting.name,
                    choices=[(k, v) for k, v in setting.choices.items()],
                    widget=forms.Select(attrs={'class': 'form-control'}),
                    help_text=setting.help_text,
                )
            self.fields[setting.id] = field

        if current_settings:
            for name, field in self.fields.items():
                field.initial = current_settings.get(name)
