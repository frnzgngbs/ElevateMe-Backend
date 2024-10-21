from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .View import *
from .View.ChannelSubmissionView import ChannelSubmissionView
from .View.ProblemStatementView import TwoVennProblemStatementView, ThreeVennProblemStatementView
from .View.RoomChannelView import RoomChannelView
from .View.RoomView import RoomView
from .View.SubmissionCommentView import SubmissionCommentView

router = SimpleRouter()
router.register('user', UserView)
router.register('ai', GPTApiView, basename='ai')
router.register('two_venn_ps', TwoVennProblemStatementView)
router.register('three_venn_ps', ThreeVennProblemStatementView)
router.register('rooms', RoomView)
router.register('channels', RoomChannelView)

submission_router = routers.NestedSimpleRouter(
    router,
    r'channels',
    lookup='channel'
)

submission_router.register(
    r'submissions',
    ChannelSubmissionView,
    basename='channel-submissions'
)

# Second Nested Router: Comments nested under Submissions
comment_router = routers.NestedSimpleRouter(
    submission_router,
    r'submissions',
    lookup='submission'
)

comment_router.register(
    r'comments',
    SubmissionCommentView,
    basename='submission-comments'
)

urlpatterns = [
    path('', include(router.urls)),  # Correct usage of include
    path('', include(submission_router.urls)),
    path('', include(comment_router.urls))
]

