from django import forms

class CreateNewPageForm(forms.Form):
    text_input = forms.CharField(label="Text Input",max_length=100)
    textarea_input = forms.CharField(label="Textarea Input", widget=forms.Textarea)

class EditPageForm(forms.Form):
    textarea_input = forms.CharField(label="Textarea Input", widget=forms.Textarea)