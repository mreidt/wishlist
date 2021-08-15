from core.models import Produto, WishlistItem
from django.contrib import admin
from django.contrib.auth import get_user_model

admin.site.register(WishlistItem)
admin.site.register(Produto)
admin.site.register(get_user_model())
