''' Course application's tests '''
from django.test import TestCase
from django.urls import reverse

class CourseListViewTest(TestCase):
    ''' Tests the homepage '''

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
