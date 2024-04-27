from django.db import models

# Create your models here.
class SignUpData(models.Model):
    sign_name=models.CharField(max_length=100,blank=False)
    sign_email=models.EmailField(max_length=100,blank=False,unique=True)
    sign_password=models.CharField(max_length=100, blank=False)
    sign_time= models.DateTimeField(blank=False, auto_now=True)

    def __str__(self):
        return self.sign_name
    class Meta:
        db_table="users_data"

class ForgotPassword(models.Model):
    email=models.EmailField(blank=False)
    class Meta:
        db_table="forgotpassword"
class Product(models.Model):
    id=models.AutoField(primary_key=True)
    category_choices = (("Dog", "Dog"), ("Cat", "Cat"), ("Bird", "Bird"), ("Fish","Fish"),("Rabbit","Rabbit"),("Gunniepig","Gunniepig"),("Shelters","Shelters"),("Medicines","Medicines"))
    category = models.CharField(max_length=100, blank=False,choices=category_choices)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=200,blank=False)
    price = models.PositiveIntegerField(blank=False)
    image = models.FileField(blank=False,upload_to="productimages")
    secure_key = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "product_table"

class Owners(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50,unique=True,blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=50,blank=False)
    secure_key = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return self.username
    class Meta:
        db_table = "owners_table"


class Contact(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    comment=models.CharField(max_length=999)
    email=models.EmailField(blank=False)

    class Meta:
        db_table="contact"

class cart(models.Model):
    mail=models.CharField(max_length=30,blank=False)
    pid=models.IntegerField(blank=False)
    def __str__(self):
        return f"{self.mail} - {self.pid}"
    class Meta:
        db_table="cart_table"
        unique_together = ('mail', 'pid')

class Cartmultipe(models.Model):
    mail = models.CharField(max_length=30, blank=False)
    pid = models.IntegerField(blank=False)
    quantity = models.IntegerField(default=1)  # Add quantity field
    # Add other fields as needed

    def __str__(self):
        return f"{self.mail} - {self.pid}"

    class Meta:
        db_table = "cartmultipleptod_table"
        unique_together = ('mail', 'pid')


class ColdCoffee(models.Model):
    name=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False)
