from django.urls import path
from .View import GPTApiView


urlpatterns = [
    path('ai/', GPTApiView.as_view()),
]

