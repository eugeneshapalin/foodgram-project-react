from http import HTTPStatus
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from api.filters import IngredientFilter, TagsFilter
from api.pagination import RecipePagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             SubscribeSerializer, SubscribtionSerializer,
                             SubscriptionRecipesSerializer, TagSerializer)
from api.models import (FavoriteList, Ingredient, IngredientInRecipe,
                        Recipe, ShoppingCart, Subscription, Tag)
from users.models import User
from foodgram_shapalin.settings import FILE
content_type = 'text/plain'


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagsFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):

        if request.method == 'POST':
            return self.add_recipe(FavoriteList, request, pk)
        return self.delete_recipe(FavoriteList, request, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request, pk)
        return self.delete_recipe(ShoppingCart, request, pk)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):

        result = IngredientInRecipe.objects.filter(
            recipe__shoppingcartrecipe__user=request.user
        ).values(
            'ingredient__name'
        ).order_by(
            'ingredient__name'
        ).annotate(
            ingredient_total=Sum('amount')
        )

        line = ''
        for item in result:
            line = line + f"{str(item['ingredient__name'])} \
                    {str(item['ingredient_total'])} \
                    {str(item['measurement_unit'])}\n"

        content = line
        response = HttpResponse(content, content_type)
        response['Content-Disposition'] = f'filename={FILE}'
        return response

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(recipe=recipe, user=request.user).exists():
            return Response(status=HTTPStatus.BAD_REQUEST)
        model.objects.create(recipe=recipe, user=request.user)
        serializer = SubscriptionRecipesSerializer(recipe)
        return Response(data=serializer.data, status=HTTPStatus.CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            model.objects.filter(
                user=request.user, recipe=recipe
            ).delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.BAD_REQUEST)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribtionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = RecipePagination

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()


class SubscribeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, id):
        author = get_object_or_404(User, id=id)
        user = self.request.user
        data = {'author': author.id, 'user': user.id}
        serializer = SubscribeSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTPStatus.CREATED)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        user = self.request.user
        subscription = get_object_or_404(
            Subscription, user=user, author=author
        )
        subscription.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
