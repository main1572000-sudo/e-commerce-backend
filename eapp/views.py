from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import generics,status,viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import ProductSerializer,CartSerializer
from .models import Cart,User,Product
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.db.models import F
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

# views.py

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    serializer_class = CartSerializer
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    # 💡 قمنا بحذف دالة add_to_cart القديمة لأن السيرياليزر في الأعلى صار يتولى المهمة بالكامل بنجاح وبشكل تلقائي!
    def destroy(self, request, *args, **kwargs):
        # 1. جلب عنصر السلة المراد حذفه قبل مسحه من قاعدة البيانات
        cart_item = self.get_object()
        product = cart_item.product
        
        # 2. إعادة الكمية المحجوزة في السلة إلى مخزن المنتج العام
        product.qty += cart_item.quantity
        product.save()
        
        # 3. إكمال عملية الحذف الافتراضية من السلة
        return super().destroy(request, *args, **kwargs)
def ping(request):
    x={
        'ping':'ping'
    }
    return JsonResponse(x)