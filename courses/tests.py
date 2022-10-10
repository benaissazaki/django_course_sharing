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


class CourseDetailViewTest(TestCase):
    ''' Tests the CourseDetailView '''

    def test_non_existent_returns_404(self):
        ''' Verifies that searching a non existent course returns a 404 response '''
        response = self.client.get('/course/nonexistentcourse')
        self.assertEqual(response.status_code, 404)

    def test_existent_returns_200(self):
        ''' Verifies that searching an existent course returns a 200 response '''
        Course.objects.create(name='Random course', pdf_file='test.pdf')
        response = self.client.get('/course/Random course')
        self.assertEqual(response.status_code, 200)

    def test_course_with_pdf_only(self):
        '''
            Verifies that a course with pdf has it embeded in the page
            and that there is no youtube embed
        '''
        Course.objects.create(name='Random course', pdf_file='test.pdf')
        response = self.client.get('/course/Random course')
        self.assertContains(response, '<embed')
        self.assertNotContains(response, '<iframe')

    def test_course_with_video_only(self):
        '''
            Verifies that a course with video has it embeded in the page
            and that there is no pdf embed
        '''
        Course.objects.create(
            name='Random course',
            youtube_video='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        response = self.client.get('/course/Random course')
        self.assertNotContains(response, '<embed')
        self.assertContains(response, '<iframe')

    def test_course_with_video_and_pdf(self):
        '''
            Verifies that a course with video and pdf
            has both embeded in the page
        '''
        Course.objects.create(
            name='Random course',
            youtube_video='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            pdf_file='test.pdf')
        response = self.client.get('/course/Random course')
        self.assertContains(response, '<embed')
        self.assertContains(response, '<iframe')


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
