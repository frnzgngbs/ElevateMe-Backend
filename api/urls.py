from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .View import *
from .View.ProblemStatementView import TwoVennProblemStatementView, ThreeVennProblemStatementView

router = SimpleRouter()
router.register('user', UserView)
router.register('ai', GPTApiView, basename='ai')
router.register('two_venn_ps', TwoVennProblemStatementView)
router.register('three_venn_ps', ThreeVennProblemStatementView)

urlpatterns = [
    path('', include(router.urls))  # Correct usage of include
]

