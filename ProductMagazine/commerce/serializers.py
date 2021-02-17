from rest_framework import serializers
from .models import Product, Wishlist, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]


class ProductModelSerializer(serializers.ModelSerializer):
    unique_wishers = serializers.SerializerMethodField(read_only=True)

    def get_unique_wishers(self, obj):
        return len(set(obj.wishlist_set.all().values_list('user')))

    class Meta:
        model = Product
        fields = ['id', 'title', 'slu', 'description', 'price', 'unique_wishers']  # '__all__'


class WishlistModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'title', 'user', 'products']




