from django.shortcuts import get_object_or_404
from rest_framework import generics, views, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Tag, Episode, EpisodeComment, EpisodeLike
from .serializers import CategorySerializer, TagSerializer, EpisodeSerializer, EpisodePostSerializer, \
    EpisodeCommentSerializer, EpisodeLikeSerializer
from .permissions import IsAuthorOrReadOnly


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EpisodeListAPIView(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    serializer_post_class = EpisodePostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return super().get_serializer_class()
        return self.serializer_post_class


class EpisodeCommentAPIView(generics.ListCreateAPIView):
    # /episode/{episode_id}/comments/
    queryset = EpisodeComment.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        ctx = super().get_serializer_class()
        episode_id = self.kwargs.get('episode_id')
        ctx['episode_id'] = episode_id
        return ctx

    def get_queryset(self):
        episode_id = self.kwargs.get('episode_id')
        qs = super().get_queryset()
        if episode_id:
            return qs.filter(episode_id=episode_id)
        return qs.none()


class EpisodeCommentDeleteAPIView(generics.DestroyAPIView):
    # /episode/{episode_id}/comments/{pk}
    queryset = EpisodeComment.objects.all()
    serializer_class = EpisodeCommentSerializer

    def get_queryset(self):
        episode_id = self.kwargs.get('episode_id')
        qs = super().get_queryset()
        if episode_id:
            return qs.filter(episode_id=episode_id)
        return qs.none()


class LikeAPIView(generics.CreateAPIView):
    queryset = EpisodeLike.objects.all()
    serializer_class = EpisodeLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
            {
                "episode_id": 2,
            }
        """
        episode_id = request.data.get('episode_id')
        user_id = request.user.id
        has_like = EpisodeLike.objects.filter(EpisodeLike, episode_id=episode_id, author_id=user_id)
        if has_like.exists():
            has_like.delete()
            return Response({"detail": "Episode removed from liked list"})
        EpisodeLike.objects.create(episode_id=episode_id, author_id=user_id)
        return Response({"detail": "Episode added to liked list"})
