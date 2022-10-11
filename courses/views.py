# pylint: disable=missing-class-docstring, missing-module-docstring
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Category, Course


class CourseListView(ListView):
    model = Course
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hierarchical_categories'] = Category.get_hierarchical_categories()
        return context

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            try:
                category_obj = Category.objects.get(name=category)
                return Category.get_category_courses(category_obj).order_by('-created_at')
            except Category.DoesNotExist:
                return self.model.objects.none()

        return self.model.objects.all().order_by('-created_at')


class CourseDetailView(DetailView):
    model = Course
    slug_field = 'name'
    slug_url_kwarg = 'name'
