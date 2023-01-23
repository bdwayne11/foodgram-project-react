from django_filters import filters, FilterSet
from recepts.models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited',)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        print(queryset)
        print(name)
        print(value)
        if value and user.is_authenticated:
            return queryset.filter(favourite__user=user)
        return queryset