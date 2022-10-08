import os
import re
from pathlib import Path
from django.test import SimpleTestCase
from django.template.loader import get_template

class TemplateTests(SimpleTestCase):
    def test_templates_correctly_set(self):
        ''' Verifies if courses_catalog/templates/index.html is detected '''
        get_template('index.html')
        
    def test_templates_no_syntax_error(self):
        ''' Verifies if all templates don't generate TemplateSyntaxError '''
        templates_path = os.path.join('.', 'templates')
        for p in Path(templates_path).rglob('*'):
            if p.suffix == '.html':
                get_template(p.relative_to(templates_path))
