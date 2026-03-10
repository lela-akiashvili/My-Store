from django.db import models
from django.contrib.auth.models import User

# 1. ნივთების ძირითადი ცხრილი
class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="დასახელება")
    brand = models.CharField(max_length=100, verbose_name="ბრენდი")
    category = models.CharField(max_length=100, verbose_name="კატეგორია")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ფასი")
    description = models.TextField(verbose_name="აღწერა")
    stock_quantity = models.IntegerField(default=0, verbose_name="რაოდენობა საწყობში")
    image = models.ImageField(upload_to='items/', null=True, blank=True, verbose_name="სურათი")
    release_date = models.DateField(null=True, blank=True, verbose_name="გამოშვების თარიღი")

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(r.rating_stars for r in reviews) / len(reviews), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()

# 2. კალათის რელაციური ცხრილი
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.item.price * self.quantity

# 3. შეფასებების ცხრილი
class ItemReview(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100, verbose_name="შემფასებლის სახელი და გვარი")
    rating_stars = models.IntegerField(default=5, verbose_name="რეიტინგი (1-5)")
    comment = models.TextField(verbose_name="კომენტარი")

    def __str__(self):
        return f"{self.reviewer_name} - {self.item.name}"