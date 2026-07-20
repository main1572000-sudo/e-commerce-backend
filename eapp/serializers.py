from rest_framework import serializers
from .models import User ,Product ,Cart

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password','email']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
#...................................................
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = '__all__'
#...................................................
class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity']
        
    def create(self, validated_data):
        # التقاط المستخدم الحالي من سياق الطلب (Context)
        user = self.context['request'].user
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)

        # تطبيق منطق get_or_create لمنع التكرار
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )

        # إذا كان المنتج موجوداً مسبقاً، نزيد الكمية بالقدر المرسل
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item