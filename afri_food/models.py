from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):   
    phone_number = models.CharField(max_length=20, null=True, blank=True)


class MarketCategory(models.Model):
    categoryName = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.categoryName)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.categoryName


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    category = models.ForeignKey(MarketCategory, on_delete=models.CASCADE, related_name="subcategories", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category}-{self.name}"


class Image(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.content_object}"


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.author} commented on {self.content_object}"


class Oil(models.Model):
    title = models.CharField(max_length=100)
    litres = models.FloatField(help_text="Enter the volume in litres")
    in_stock = models.BooleanField(default=True, help_text="Is this item in stock?")
    price = models.FloatField(help_text="Enter the price of the item")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    images = GenericRelation(Image)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"{self.title} {self.litres} litres - ${self.price} {self.subcategory} - {'In Stock' if self.in_stock else 'Out of Stock'}"


class CrayFish(models.Model):
    title = models.CharField(max_length=100)
    kg = models.FloatField(help_text="Enter the weight in kg")
    in_stock = models.BooleanField(default=True, help_text="Is this item in stock?")
    price = models.FloatField(help_text="Enter the price of the item")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    images = GenericRelation(Image)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"{self.title} {self.kg} kg - ${self.price} {self.subcategory} - {'In Stock' if self.in_stock else 'Out of Stock'}"


class CatFish(models.Model):
    title = models.CharField(max_length=100)
    kg = models.FloatField(help_text="Enter the weight in kg")
    in_stock = models.BooleanField(default=True, help_text="Is this item in stock?")
    price = models.FloatField(help_text="Enter the price of the item")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    images = GenericRelation(Image)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"{self.title} {self.kg} kg - ${self.price} {self.subcategory} - {'In Stock' if self.in_stock else 'Out of Stock'}"


class PonmoByKg(models.Model):
    title = models.CharField(max_length=100)
    kg = models.FloatField(help_text="Enter the weight in kg")
    in_stock = models.BooleanField(default=True, help_text="Is this item in stock?")
    price = models.FloatField(help_text="Enter the price of the item")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    images = GenericRelation(Image)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"{self.title} {self.kg} kg - ${self.price} {self.subcategory} - {'In Stock' if self.in_stock else 'Out of Stock'}"


class PonmoByPiece(models.Model):
    title = models.CharField(max_length=100)
    piece = models.FloatField(help_text="Enter the number of pieces")
    in_stock = models.BooleanField(default=True, help_text="Is this item in stock?")
    price = models.FloatField(help_text="Enter the price per piece")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    images = GenericRelation(Image)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"{self.title} {self.piece} pieces - ${self.price} {self.subcategory} - {'In Stock' if self.in_stock else 'Out of Stock'}"
    


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.content_object} - {self.quantity}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order from Username: {self.user.username}; Email: {self.user.email}; Phone Number: {self.user.phone_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.content_object} - {self.quantity}"

