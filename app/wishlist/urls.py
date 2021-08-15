from django.urls import include, path
from rest_framework.routers import DefaultRouter

from wishlist import views

router = DefaultRouter()
router.register('wishlist', views.WishlistItemViewSet)

app_name = 'wishlist'
urlpatterns = [
    path('', include(router.urls))
]
