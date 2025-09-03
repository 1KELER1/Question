from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from typing import List
from django.urls.resolvers import URLPattern

from .views import (
    QuestionListCreateView,
    QuestionDetailView,
    AnswerDetailView,
    create_answer
)

app_name: str = 'qa_api'

urlpatterns: List[URLPattern] = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:question_id>/answers/', create_answer, name='create-answer'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
