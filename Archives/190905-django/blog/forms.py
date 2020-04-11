from django import forms

class AucForm(forms.Form):
  post = forms.IntegerField(label='Year')