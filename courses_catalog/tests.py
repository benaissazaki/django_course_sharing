''' Global tests '''
import os
from pathlib import Path
from django.test import SimpleTestCase
from django.template.loader import get_template
from django.urls import reverse


class TemplateTests(SimpleTestCase):
    ''' Tests the template settings '''

    def test_templates_correctly_set(self):
        ''' Verifies if courses_catalog/templates/index.html is detected '''
        get_template('index.html')

    def test_templates_no_syntax_error(self):
        ''' Verifies if all templates don't generate TemplateSyntaxError '''
        templates_path = os.path.join('.', 'templates')
        for path in Path(templates_path).rglob('*'):
            if path.suffix == '.html':
                get_template(path.relative_to(templates_path))


class HomePageTests(SimpleTestCase):
    ''' Tests the homepage '''

    def test_url_exists_at_correct_location(self):
        ''' Verifies the homepage exists '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        ''' Verifies the url can be accessed via name '''
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        ''' Verifies the right template is used '''
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "index.html")
