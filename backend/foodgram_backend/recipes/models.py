from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField('Название', max_length=256, unique=True)
    color = models.CharField(
        'HEX-код цвета',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Неверные данные! Необходимо ввести в формате HEX!'
            )
        ]
    )
    slug = models.SlugField('Ссылка', max_length=256, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField('Название', max_length=256)
    measurement_unit = models.CharField('Единица измерения',
                                        max_length=256)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    image = models.ImageField('Картинка',
                              upload_to='recipe')
    cooking_time = models.IntegerField(
        'Время в минутах',
        validators=[
            MinValueValidator(1, message='Минимальное время - 1 минута!')
        ]
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Тег'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.SET_DEFAULT,
        default='Удаленный пользователь',
        null=True, verbose_name='Автор', related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredients, through='IngredientsRecipes', related_name='recipes',
        verbose_name='Ингридиенты'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsRecipes(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredients, on_delete=models.CASCADE,
        verbose_name='Ингридиент в рецепте',
    )
    amount = models.IntegerField(
        'Количество в шт',
        validators=[
            MinValueValidator(1, message='Минимальное значение 1')
        ]
    )

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецептах'

    def __str__(self):
        return (f'{self.ingredient.name} ({self.ingredient.measurement_unit}):'
                f'{self.amount} шт.')


class Favourites(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
        related_name='favourite'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
        related_name='favourite'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class Basket(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
        related_name='basket'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
        related_name='basket'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина с покупками'
        verbose_name_plural = 'Корзины с покупками'

    def __str__(self):
        return f'{self.user} добавил в корзину с покупками {self.recipe}'
