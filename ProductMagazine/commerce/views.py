import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from drf_util.decorators import serialize_decorator
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Product, Wishlist, User
from .serializers import ProductModelSerializer, WishlistModelSerializer, RegisterSerializer


# Create your views here.


def home(request):
    home_template = loader.get_template("commerce/home.html")
    context = {}
    return HttpResponse(home_template.render(context, request))
    # return redirect("schema-swagger-ui")


def products(request):
    index_template = loader.get_template("commerce/products.html")

    wishlists = Wishlist.objects.filter(user_id=request.user.id)

    # Create extra attribute for each object in wishlists to make a comparison check in template
    for wishlist in wishlists:
        wishlist.products_ids = wishlist.products.values_list('id', flat=True)

    # Get and set unique_wishers for each product
    products = Product.objects.all()
    for product in products:
        product.unique_wishers = Wishlist.objects.filter(products__id=product.id).values_list('user', flat=True).distinct().count()
        product.save()

    context = {'products': products, 'wishlists': wishlists}
    return HttpResponse(index_template.render(context, request))


def login_view(request):
    if request.method == "GET":
        return render(request, "commerce/login.html")

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:  # is not None:
            login(request, user)
            return redirect("products")
        else:
            return render(request, "commerce/login.html", {
                "message": "Invalid credentials."
            })


def logout_view(request):
    logout(request)
    return redirect('products')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "commerce/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "commerce/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('products')
    else:
        return render(request, "commerce/register.html")


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(RegisterSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            is_staff=False
        )
        user.set_password(validated_data.get('password'))
        user.save()

        return Response(RegisterSerializer(user).data)


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class WishlistsViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistModelSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    # def get_permissions(self):
    #     # if self.action == ['list', 'retrieve']:
    #     permission_classes = [IsAuthenticated]
    #     if self.action == ['create', 'update', 'destroy', 'partial_update']:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

    #
    # def list(self, request, *args, **kwargs):
    #
    #     # self.queryset.filter(user_id=request.user.id)
    #     # print(type(self.serializer_class(self.queryset.filter(user_id=request.user.id), many=True).data))
    #     # print(self.serializer_class(self.queryset.filter(user_id=request.user.id), many=True).data)
    #
    #     return Response(self.serializer_class(self.queryset, many=True).data)


class WishlistView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        wishlists_template = loader.get_template("commerce/wishlists.html")

        context = {'wishlists': Wishlist.objects.filter(user_id=request.user.id)}
        return HttpResponse(wishlists_template.render(context, request))

    # Create new wishlist by JS fetch-request
    def post(self, request):

        data = json.loads(request.body)
        wishlist_title = data.get('wishlist_title')

        new_wishlist = Wishlist.objects.create(user_id=request.user.id, title=wishlist_title)
        data = {"id": int(new_wishlist.id), "title": str(new_wishlist.title), "user": str(new_wishlist.user_id)}
        return JsonResponse(data)

    # Modify existing wishlist by JS fetch-request
    def put(self, request):

        data = json.loads(request.body)
        product_id = data.pop('product_id')
        product = Product.objects.get(id=product_id)

        for key, value in data.items():
            wishlist_id = key
            to_do = value
            wishlist = Wishlist.objects.get(id=wishlist_id)

            if to_do:
                wishlist.products.add(product)
            else:
                wishlist.products.remove(product)

            wishlist.save()

        return HttpResponse(status=204)

    # Delete a wishlist with all content
    def delete(self, request):
        data = json.loads(request.body)
        wishlist_id = data.get('wishlist_id')

        Wishlist.objects.get(id=wishlist_id).delete()

        return HttpResponse(status=204)


# class RegisterView(View):
#
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             data = {
#                 "first_name": form.cleaned_data.get('first_name'),
#                 "last_name": form.cleaned_data.get('last_name'),
#                 "email": form.cleaned_data.get('email'),
#                 "username": form.cleaned_data.get('username')
#             }
#             return JsonResponse(data, status=201)
#
#         else:
#             return JsonResponse(form.data, status=406)