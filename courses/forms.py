''' Courses app's forms '''

from typing import List
from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Exam, Course


class SearchForm(forms.Form):
    ''' Form to search for courses '''
    query = forms.CharField(label='Query',
                            max_length=100)


class ExamAdminForm(forms.ModelForm):
    ''' Exam creation form for admin page '''
    class Meta:
        model = Exam
        fields = '__all__'

    def clean(self):
        ''' Verifies that either related courses or categories are specified '''
        related_courses: List[Course] = self.cleaned_data.get(
            'related_courses')
        categories = self.cleaned_data.get('categories')

        if not related_courses and not categories:
            raise ValidationError(
                'You must either specify related courses or categories')
        for course in related_courses:
            # Give the exam the same categories as its related courses
            category = Category.objects.filter(id__in=course.categories.all())
            self.cleaned_data['categories'] = self.cleaned_data.get(
                'categories').union(category)

        return self.cleaned_data
