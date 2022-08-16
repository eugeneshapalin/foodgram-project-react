from django.contrib import admin
from api.models import (FavoriteList, Ingredient,
                        IngredientInRecipe, Recipe,
                        ShoppingCart, Subscription, Tag)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )
    list_display_links = ('recipe',)
    search_fields = ('recipe__name', 'ingredient__name')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name__istartswith', 'name__contains')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(
            IngredientAdmin, self
        ).get_search_results(request, queryset, search_term)
        queryset1 = queryset.filter(name__istartswith=search_term)
        queryset2 = queryset.filter(name__contains=search_term)
        queryset = queryset1.union(queryset2, all=True)
        return queryset, use_distinct


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInline,)
    list_display = ('author', 'name', 'count_favorite')
    list_filter = ('author', 'tags')
    search_fields = ('name', 'author__username')

    def count_favorite(self, obj):
        return FavoriteList.objects.filter(recipe=obj).count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name',)


class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = (
        'user__username',
        'user__email'
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(FavoriteList, FavoriteListAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
