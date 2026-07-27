from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import generics,status,viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import ProductSerializer,CartSerializer
from .models import Cart,User,Product
from rest_framework.views import APIView
from django.contrib.auth import get_user_model  # ✅ استيراد دالة جلب النموذجfrom rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
# Create your views here.
User = get_user_model()  # ✅ جلب النموذج المخصص الخاضع لمشروعك
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Please provide username, password, and email'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. إنشاء المستخدم بحالة غير مفعلة
        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_active = False
        user.save()

        # 2. تشفير معرّف المستخدم (uid) وتوليد التوكن (token)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # نرسل الـ uid والـ token معاً في الرابط مقسومين بـ slash
        verification_link = f"http://localhost:3000/verify-email/{uid}/{token}"

        try:
            send_mail(
                subject='Activate Your Account',
                message=f'Hello {username},\n\nPlease click the link below to activate your account:\n{verification_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            user.delete()
            return Response({'error': 'Failed to send verification email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {'message': 'User created successfully. Please check your email to activate your account.'},
            status=status.HTTP_201_CREATED
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')

        if not uidb64 or not token:
            return Response({'error': 'UID and Token are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # فك تشفير ID المستخدم
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # التحقق من صحة التوكن والمستخدم
        if user is not None and default_token_generator.check_token(user, token):
            if user.is_active:
                return Response({'message': 'Account is already activated.'}, status=status.HTTP_200_OK)

            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully! You can now log in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired activation link.'}, status=status.HTTP_400_BAD_REQUEST)
def generate_verification_token(user):
    # ننشئ AccessToken مخصص ونضيف فيه معرّف المستخدم
    token = AccessToken.for_user(user)
    # يمكنك إضافة مؤشر خاص للتأكد أن هذا التوكن مخصص للتفعيل فقط
    token['token_type'] = 'email_verification'
    return str(token)

        
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

