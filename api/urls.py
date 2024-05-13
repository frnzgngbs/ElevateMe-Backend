from django.urls import path
from .View import *

urlpatterns = [
    path('ai/', GPTApiView.as_view()),
    path('user/', UserView.as_view())
]

