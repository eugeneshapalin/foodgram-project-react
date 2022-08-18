from colorfield.fields import ColorField
from django.db import models
from users.models import User
from django.core import validators
from foodgram_shapalin.settings import MIN_TIME,MAX_TIME


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='название',
    )
    color = ColorField(
        unique=True,
        verbose_name='цвет',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='id',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='единица измерения',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='название',
    )
    image = models.ImageField(
        blank=True,
        verbose_name='изображение',
        help_text='загрузите изображение',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='тег',
    )
    time = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                MIN_TIME, message='минимальное время приготовления 1 минута'),
            validators.MaxValueValidator(
                MAX_TIME, message='максимальное время приготовления 24 часа'),),
        verbose_name='время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата публикации'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_recipe_author'
            ),
        )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
        verbose_name='ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
        verbose_name='рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                MIN_TIME, message='минимальное количество ингредиентов - 1'),
            validators.MaxValueValidator(
                MAX_TIME, message='превышено максимальное количество ингредиентов'),),
    )

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецепте'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredientinrecipe'
            ),
        )

    def __str__(self):
        return f'ингредиент {self.ingredient} в {self.recipe}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор'
    )
    
    class Meta:
        verbose_name = 'подписка'
        constraints = (
            models.CheckConstraint(
                check=models.Q(User.username != Recipe.author),
                name='невозможно подписаться на самого себя',),
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
        )

    def __str__(self):
        return (
            f'пользователь {self.user} '
            f'подписан на {self.author}'
        )


class FavoriteList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoritelist',
        verbose_name='подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favoriterecipe',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'список избранного'
        verbose_name_plural = 'списки избранного'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'
            ),
        )

    def __str__(self):
        return (
            f'пользователь {self.user} '
            f'добавил в избранное рецепт "{self.recipe}"'
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcartrecipe',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shoppingcart_recipe'
            ),
        )

    def __str__(self):
        return (
            f'пользователь {self.user} '
            f'добавил в список покупок "{self.recipe}"'
        )
