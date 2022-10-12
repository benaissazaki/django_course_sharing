''' Courses app's forms '''

from django import forms

class SearchForm(forms.Form):
    ''' Form to search for courses '''
    query = forms.CharField(label='Query', max_length=100)
