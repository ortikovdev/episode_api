from rest_framework import serializers
from .models import Category, Tag, Episode, EpisodeComment, EpisodeLike
from ..account.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class EpisodeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Episode
        fields = ['id', 'title', 'slug', 'author', 'image', 'music', 'category', 'description', 'tags', 'created_date']


class EpisodePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'slug', 'author', 'image', 'music', 'description', 'tags', 'created_date']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['author_id'] = request.user.id
        return super().create(validated_data)


class EpisodeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeComment
        fields = ['id', 'author', 'episode', 'comment', 'parent', 'top_level_comment_id', 'created_date']
        read_only_fields = ['top_level_comment_id']

    def create(self, validated_data):
        episode_id = self.context['episode_id']
        validated_data['episode_id'] = episode_id
        return super().create(validated_data)


class EpisodeLikeSerializer(serializers.Serializer):
    episode_id = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ['episode_id']
