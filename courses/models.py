# pylint: disable=invalid-str-returned
''' Models for the courses app '''
from django.db import models
from django.db.models import Q
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
