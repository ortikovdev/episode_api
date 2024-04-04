from rest_framework import generics, views, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Tag, Episode, EpisodeComment, EpisodeLike
from .serializers import CategorySerializer, TagSerializer, EpisodeCommentSerializer, EpisodeSerializer, EpisodePostSerializer, EpisodeCommentSerializer
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
