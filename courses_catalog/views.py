''' Global views '''
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    ''' Homepage view '''
    template_name = 'index.html'
