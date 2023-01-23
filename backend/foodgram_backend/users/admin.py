from django.contrib import admin

from .models import CustomUser, Subscribe

admin.site.register(CustomUser)
admin.site.register(Subscribe)
