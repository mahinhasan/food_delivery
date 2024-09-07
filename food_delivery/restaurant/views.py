from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CategorySerializer, MenuItemSerializer, OrderSerializer,RestaurantSerializer
from .models import User, Category, MenuItem,Restaurant
from .permissions import IsOwnerOrEmployee, IsRestaurantUser



# user resitrations api
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


# login api
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
   
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data}, status=200)
    return Response({"error": "Invalid credentials"}, status=400)



# creat category list api
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.filter(restaurant=request.user.restaurant)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=request.user.restaurant)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



# create menu item api
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menu_item_list_create(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.filter(category__restaurant=request.user.restaurant)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# create direct order foot api using payment 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# create and list food resturant api
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def restaurant_list_create(request):
    if request.method == 'GET':
        # Get restaurants that the current user owns or is an employee at
        restaurants = Restaurant.objects.filter(owner=request.user) | Restaurant.objects.filter(employees=request.user)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user) 
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# restaurant details,update,delete api
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def restaurant_detail(request, pk):
    try:
        restaurant = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=404)

    # Check if the current user is the owner or an employee
    if request.user != restaurant.owner and request.user not in restaurant.employees.all():
        return Response({"error": "You do not have permission to access this restaurant"}, status=403)

    if request.method == 'GET':
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        restaurant.delete()
        return Response(status=204)
