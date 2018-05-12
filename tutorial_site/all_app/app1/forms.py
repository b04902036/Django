from django import forms

class FileForm(forms.Form):
	file_text = forms.CharField(label='file name', max_length = 100)
	file = forms.FileField()