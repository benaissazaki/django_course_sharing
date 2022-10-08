# pylint: disable=invalid-str-returned
''' Models for the courses app '''
from django.db import models

class Category(models.Model):
    ''' The hierarchical categories to which a course belongs '''
    name = models.CharField(max_length=100)
    father_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    ''' Courses with a youtube video and/or pdf associated '''
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    youtube_video = models.URLField(max_length=100, null=True, blank=True)
    pdf_file = models.FileField(upload_to='courses', null=True, blank=True)

    def __str__(self):
        return self.name
