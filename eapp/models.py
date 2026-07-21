from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    email= models.EmailField(unique=True,null=False,max_length=35)
    REQUIRED_FIELDS= ['email']
    
class Product(models.Model):
    x=[
        ('EL','electrics'),
        ('CL','clothes'),
        ('KT','kitchen')
    ]
    name = models.CharField(max_length=25)
    price = models.DecimalField(decimal_places=2,max_digits=7)
    category = models.CharField(choices=x)
    qty = models.IntegerField(default=1)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    description= models.TextField()
    created_at = models.DateTimeField(timezone.now())
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        # هذا السطر يجعل قاعدة البيانات ترفض تماماً تكرار نفس المنتج لنفس المستخدم
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_cart')
        ]
