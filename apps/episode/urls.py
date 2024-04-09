from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryListAPIView, TagListAPIView, EpisodeListAPIView, EpisodeCommentAPIView, \
    EpisodeCommentDeleteAPIView, LikeAPIView

router = DefaultRouter()

router.register('actions', EpisodeListAPIView)
urlpatterns = [
    path('categroy/list/', CategoryListAPIView.as_view()),
    path('tag/list/', TagListAPIView.as_view()),
    path('<int:episode_id>/comments/', EpisodeCommentAPIView.as_view()),
    path('<int:episode_id>/comments/<int:pk>/', EpisodeCommentDeleteAPIView.as_view()),
    path('like/', LikeAPIView.as_view()),
    path('', include(router.urls))
]

"""
Category:
    -list
Tag:
    -list
Episode:
    -list
    -detail
    -create
    -update
    -like
    -delete
EpisodeComment:
    -list
    -crete
    -delete
EpisodeLike
    -like
    -dislike
    
6 ta serializer
7 ta view
"""