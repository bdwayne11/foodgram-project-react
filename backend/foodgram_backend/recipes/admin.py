from django.contrib import admin

from recipes.models import (Basket, Favourites, Ingredients,
                            IngredientsRecipes, Recipe, Tag)


class RecipeIngredientAdmin(admin.StackedInline):
    model = IngredientsRecipes
    autocomplete_fields = ('ingredient',)
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'added_to_favorites')
    search_fields = ('name', 'author__email', 'tags__name')
    inlines = (RecipeIngredientAdmin,)

    @admin.display(description='Количество в избранных у пользователя')
    def added_to_favorites(self, obj):
        return obj.favourite.count()


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(IngredientsRecipes)
admin.site.register(Favourites)
admin.site.register(Basket)
