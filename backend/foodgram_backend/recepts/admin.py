from django.contrib import admin

from recepts.models import (Basket, Favourites, Ingredients,
                            IngredientsRecipes, Recipe, Tag)

admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(Recipe)
admin.site.register(IngredientsRecipes)
admin.site.register(Favourites)
admin.site.register(Basket)
