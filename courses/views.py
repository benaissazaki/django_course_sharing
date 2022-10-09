# pylint: disable=missing-class-docstring, missing-module-docstring
from django.views.generic.list import ListView
from .models import Course

class CourseListView(ListView):
    model = Course
    paginate_by = 10
