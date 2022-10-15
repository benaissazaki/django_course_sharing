# pylint: disable=invalid-str-returned
''' Models for the courses app '''
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
import regex as re

from courses.validators import PDFFileValidator


class Category(models.Model):
    ''' The hierarchical categories to which a course belongs '''
    name = models.CharField(max_length=100, unique=True)
    father_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_hierarchical_categories():
        ''' Returns categories in hierarchical form as a dict '''
        categories = Category.objects.all()
        root_categories = [
            cat for cat in categories if not cat.father_category]

        def get_children_hierarchy(category: Category):
            children = category.category_set.all()
            if not children:
                return None
            children_hierarchy = {}
            for child in children:
                children_hierarchy[child] = get_children_hierarchy(child)
            return children_hierarchy

        return {cat: get_children_hierarchy(cat) for cat in root_categories}

    @classmethod
    def get_category_courses(cls, category):
        ''' Returns courses belonging to the category or its children '''
        courses = Course.objects.filter(category=category)
        children_categories = category.category_set.all()
        if not children_categories:
            return courses

        for child in children_categories:
            courses = courses.union(cls.get_category_courses(child))
        return courses


class Course(models.Model):
    ''' Courses with a youtube video and/or pdf associated '''
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    youtube_video = models.URLField(
        max_length=100, null=True, blank=True)
    pdf_file = models.FileField(
        upload_to='courses',
        null=True,
        blank=True,
        validators=[PDFFileValidator(max_size=(1024**2)*settings.MAX_PDF_SIZE_MB)])

    class Meta:
        ''' Class defined to add constraints on Course model '''
        constraints = [
            models.CheckConstraint(
                check=Q(youtube_video__isnull=False) | ~Q(
                    pdf_file__exact=''),
                name='video-or-pdf'
            )
        ]

    def __str__(self):
        return self.name

    def get_video_id(self):
        ''' Uses regex to get the youtube video's id '''
        if self.youtube_video:
            youtube_id_regex = r'(?<=watch\?v=|/videos/|embed\/|youtu.be\/|\/v\/|watch\?v%3D|%2Fvideos%2F|embed%2F|youtu.be%2F|%2Fv%2F)[^#\&\?\n]*'  # pylint: disable=line-too-long
            return re.search(youtube_id_regex, self.youtube_video).group(0)

        return None

    def get_video_embed_url(self):
        ''' Constructs the youtube embed url '''
        if self.youtube_video:
            video_id = self.get_video_id()
            return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0"

        return None

    @classmethod
    def search_courses(cls, search_query: str):
        ''' Search for courses whose name or ancestor categories contain search_query '''
        result_courses = cls.objects.filter(name__icontains=search_query)

        def search_courses_in_category(category: Category):
            children_categories = category.category_set.all()
            related_courses = category.course_set.all()
            for child in children_categories:
                related_courses = related_courses.union(
                    search_courses_in_category(child))

            return related_courses

        matching_categories = Category.objects.filter(
            name__icontains=search_query)
        if matching_categories:
            for cat in matching_categories:
                result_courses = result_courses.union(
                    search_courses_in_category(cat))
        return result_courses


class Exam(models.Model):
    ''' Exams with a pdf file associated '''
    name = models.CharField(max_length=100, unique=True)
    related_course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    pdf_file = models.FileField(upload_to='exams',
                                validators=[
                                    PDFFileValidator(
                                        max_size=(1024**2)*settings.MAX_PDF_SIZE_MB)
                                ])
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(related_course__isnull=False) |
                    Q(category__isnull=False)
                ),
                name='course_or_category'
            )
        ]

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Exam)
def set_corresponding_category(sender, instance: Exam, *args, **kwargs): # pylint: disable=unused-argument
    ''' Set the exam's category to the related_course's '''
    if instance.related_course:
        instance.category = instance.related_course.category
