# pylint: disable=no-member
''' Course application's tests '''
from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from .models import Course


class CourseListViewTest(TestCase):
    ''' Tests the CourseListView '''

    def test_url_exists_at_correct_location(self):
        ''' Verifies the view exists '''
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        ''' Verifies the url can be accessed via name '''
        response = self.client.get(reverse("course-list"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        ''' Verifies the right template is used '''
        response = self.client.get(reverse("course-list"))
        self.assertTemplateUsed(response, "courses/course_list.html")


class CourseModelTest(TestCase):
    ''' Tests the Course model '''

    def test_video_or_pdf(self):
        '''
            Verifies that an exception is thrown when creating a course without
            a video or a pdf
        '''
        with self.assertRaises(IntegrityError):
            Course.objects.create(name='TestCourse')

    def test_can_create_with_video(self):
        ''' Verifies that a course can be created with a video only '''
        Course.objects.create(
            name='TestCourse', youtube_video='https://www.youtube.com/watch?v=HtSuA80QTyo')

    def test_can_create_with_pdf(self):
        ''' Verifies that a course can be created with a pdf only '''
        Course.objects.create(
            name='TestCourse', pdf_file='test.pdf')
