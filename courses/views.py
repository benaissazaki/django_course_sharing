# pylint: disable=missing-class-docstring, missing-module-docstring
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Course


class CourseListView(ListView):
    model = Course
    paginate_by = 10
    ordering = ['-created_at']


class CourseDetailView(DetailView):
    model = Course
    slug_field = 'name'
    slug_url_kwarg = 'name'
