from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegisterView # استيراد الفيو الجديد
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register('items',views.CartViewSet,basename='cart') # طبعا كما تعلم : لاضافة منتج الى السلة cart/items/ < POST

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('',views.Product_view.as_view(),name = 'products'),# اظهار جميع المنتجات للجميع
    path('clothes/',views.clothes_view.as_view(),name = 'only_clothes'),# اظهار جميع المنتجات الملابس للجميع
    path('electrics/',views.electrics_view.as_view(),name = 'only_electrics'),# اظهار جميع المنتجات الكهربائية للجميع
    path('kitchen/',views.kitchen_view.as_view(),name = 'only_kitchen'),# اظهار جميع المنتجات (المطبخ )للجميع
    path('cart/',include(router.urls)), # السلة 
    path('ping/',views.ping,name='ping')
]