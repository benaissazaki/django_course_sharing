''' Courses application's urls '''
from django.urls import path
from .views import CourseDetailView, CourseListView, ExamListView, ExamDetailView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('<str:name>', CourseDetailView.as_view(), name='course-detail'),
    path('exam/', ExamListView.as_view(), name='exam-list'),
    path('exam/<str:name>', ExamDetailView.as_view(), name='exam-detail')
]
