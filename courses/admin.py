# pylint: disable=missing-class-docstring, missing-module-docstring
from typing import Any, Optional
from django.contrib import admin

from courses.forms import ExamAdminForm
from .models import Category, Course, Exam


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'father_category')
    list_filter = ('father_category',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = ExamAdminForm
