from django.contrib import admin
from django.urls import path

from .views.user import UserViewSurvey, UserResults, UserSurveyResults
from .views.admin import AdminSurvey, AdminQuestionInSurvey

app_name = "survey"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('', UserViewSurvey.as_view()),
    path('<int:s_id>', UserViewSurvey.as_view()),
    path('results/<int:u_id>', UserResults.as_view()),
    path('results/<int:u_id>/survey/<int:s_id>', UserResults.as_view()),
    path('results/survey/<int:s_id>', UserSurveyResults.as_view()), 
    path('survey/', AdminSurvey.as_view()),
    path('survey/<int:s_id>', AdminSurvey.as_view()),
    path('survey/<int:s_id>/questions/', AdminQuestionInSurvey.as_view()),
    path('survey/<int:s_id>/questions/<int:q_id>', AdminQuestionInSurvey.as_view()),
]