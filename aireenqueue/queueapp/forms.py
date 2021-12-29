from django import forms

class Newcomer(forms.Form):
    number = forms.IntegerField(required=False)