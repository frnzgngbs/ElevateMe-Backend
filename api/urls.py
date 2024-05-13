from django.template.defaulttags import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .View import *

router = SimpleRouter()
router.register('user', UserView)
router.register('ai', GPTApiView, basename='ai')

urlpatterns = [
    path('', include(router.urls))  # Correct usage of include
]

