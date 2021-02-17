
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .yasg import urlpatterns as doc_urls


router = routers.SimpleRouter()
router.register(r'product', views.ProductsViewSet)
router.register(r'wishlist', views.WishlistsViewSet)


urlpatterns = [
    path('', views.home, name="home"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("register", views.register, name="register"),
    path('DRF-register', views.RegisterView.as_view(), name='drf_register'),

    path("products", views.products, name="products"),
    path("wishlists", views.WishlistView.as_view(), name="wishlists"),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += router.urls
urlpatterns += doc_urls

