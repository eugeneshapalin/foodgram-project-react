from django_filters import rest_framework as filter

from api.models import Ingredient, Recipe, Tag
from users.models import User

class IngredientFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class TagsFilter(filter.FilterSet):
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filter.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filter.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filter.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favoriterecipe__user=self.request.user)
        return queryset.exclude(favoriterecipe__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoppingcartrecipe__user=self.request.user)
        return queryset.exclude(shoppingcartrecipe__user=self.request.user)
