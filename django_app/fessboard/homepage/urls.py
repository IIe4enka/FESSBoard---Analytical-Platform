from django.urls import path
from .views import *
urlpatterns = [
    path('', homepage),
    path('company-form/', createCompany, name='company-form'),
    path('student-form/', student_view, name='student-form'),
    path('universities-form/', student_view, name='universities-form'),
    path('teachers-form/', student_view, name='teachers-form'),
    path('events-form/', student_view, name='events-form'),
    path('projects-form/', add_project, name='projects-form'),
    path('projects-form/add-groups/', add_groups_and_students_view, name='add-groups-project-form'),
    path('company-hub/', companyHub, name='company-hub'),
    path('update-company-form/<str:pk>/',updateCompany, name='update-company-form'),
    path('delete-company-form/<str:pk>/',deleteCompany, name='delete-company-form'),
    #path('to-form/',)
]