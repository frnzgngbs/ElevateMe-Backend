from django.template.defaulttags import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .View import *

router = SimpleRouter()
router.register('user', UserView)

urlpatterns = [
    path('ai/', GPTApiView.as_view()),
    path('', include(router.urls))  # Correct usage of include
]

