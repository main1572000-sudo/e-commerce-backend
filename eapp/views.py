from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import generics,status,viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import ProductSerializer,CartSerializer,UserSerializer
from .models import Cart,User,Product
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny] # للسماح للجميع بإنشاء حساب بدون توكن

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # إنشاء المستخدم وتشفير كلمة المرور بشكل آمن
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class Product_view(generics.ListAPIView):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
category=Product.category
class clothes_view(generics.ListAPIView):
    queryset= Product.objects.filter(category='CL')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class electrics_view(generics.ListAPIView):
    queryset= Product.objects.filter(category='EL')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class kitchen_view(generics.ListAPIView):
    queryset= Product.objects.filter(category='KT')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class CartViewSet(viewsets.ModelViewSet):
    # فرض تسجيل الدخول أولاً لضمان وجود مستخدم
    permission_classes = [IsAuthenticated] 
    serializer_class = CartSerializer
    def get_queryset(self):
        # السيرفر يجلب فقط البيانات التي تخص هذا المستخدم تحديداً
        return Cart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
    # إجبار السيرفر على حفظ request.user في حقل user في قاعدة البيانات
        serializer.save(user=self.request.user)
        
def ping(request):
    x={
        'ping':'ping'
    }
    return JsonResponse(x)