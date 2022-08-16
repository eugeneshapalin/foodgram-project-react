from django.core.validators import MinValueValidator
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import (FavoriteList, Ingredient,
                        IngredientInRecipe, Recipe, ShoppingCart,
                        Subscription, Tag)
from users.models import User
from users.serializers import CurrentCustomUserSerializer


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = request.user
        if request is None or request.user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'unit')

    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.unit = validated_data.get(
            'unit',
            instance.unit
        )
        instance.save()
        return instance

    def to_internal_value(self, data):
        return get_object_or_404(Ingredient, id=data)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = IngredientSerializer()
    name = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    amount = serializers.IntegerField(
        validators=(MinValueValidator(1),)
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'unit')

    def to_representation(self, instance):
        data = IngredientSerializer(instance.ingredient).data
        data['amount'] = instance.amount
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance

    def to_internal_value(self, data):
        return Tag.objects.get(id=data)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = AuthorSerializer(default=CurrentCustomUserSerializer())
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe',
        many=True
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )
    image = Base64ImageField(required=False)
    time = serializers.IntegerField(
        validators=(MinValueValidator(1),)
    )

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'time'
                  )
        validators = (
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name', 'author')
            ),
        )

    def ingredint_in_recipe_bulk_create(self, ingredients, recipe):
        ingredients_in_recipe = [
            IngredientInRecipe(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipe)

    def get_is_favorited(self, obj):
        request = self.context['request']
        if request is None or request.user.is_anonymous:
            return False
        return FavoriteList.objects.filter(
            user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientinrecipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self.ingredint_in_recipe_bulk_create(
            ingredients=ingredients, recipe=recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientinrecipe')
        instance.tags.set(tags)
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)

        self.ingredint_in_recipe_bulk_create(
            ingredients=ingredients, recipe=instance)

        instance.refresh_from_db()
        return instance

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                'Обязательное поле.'
            )
        if len(data) < 1:
            raise serializers.ValidationError(
                'Не переданы ингредиенты.'
            )

        ingredients = data.get('ingredientinrecipe')
        ingredient_list = []
        return data


class SubscriptionRecipesSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'time'
                  )


class SubscribtionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = Subscription

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = Recipe.objects.filter(
                author=obj.author)[:recipes_limit]
        else:
            queryset = Recipe.objects.filter(
                author=obj.author)
        return SubscriptionRecipesSerializer(
            queryset, many=True
        ).data


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'user', 'author')
        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author')
            ),
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = SubscribtionSerializer(
            instance,
            context=context
        )
        return serializer.data

    def validate_author(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя')
        return value
