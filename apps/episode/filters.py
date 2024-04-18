from django_filters import rest_framework as filters
from apps.episode.models import Episode, Tag


class EpisodeFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags',
        to_field_name='name',
        method='filter_by_tags'
    )

    def filter_by_tags(self, queryset, name, value):
        if value:
            tag_ids = [int(id) for id in value.split(',')]
            queryset = queryset.filter(tags__in=tag_ids)
        return queryset

    class Meta:
        model = Episode
        fields = ['category', 'tags']
