from django.contrib import admin

from recepts.models import (Tag, Ingredients, Recipe,
                            IngredientsRecipes, Favourites,
                            Basket)

admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(Recipe)
admin.site.register(IngredientsRecipes)
admin.site.register(Favourites)
admin.site.register(Basket)
