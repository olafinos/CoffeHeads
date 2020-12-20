from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Coffee(models.Model):
    """
    Basic class for coffee
    """

    name = models.CharField(max_length=250, help_text="Enter full name of coffee")
    origin = models.CharField(max_length=100, help_text="Enter coffee origin")
    manufacturer = models.CharField(max_length=150, help_text="Enter coffee manufacturer")
    description = models.TextField(blank=True, help_text="Enter coffee description")
    average = models.FloatField(blank=True, default=0.0)
    reviewed_by = models.IntegerField(default=0, blank=True)
    image = models.ImageField(
        upload_to="img", default="img/default_coffee.jpg", null=True, blank=True
    )
    estimated_price = models.FloatField(default=0,blank=True)
    add_date = models.DateField(
        default=timezone.now().strftime("%Y-%m-%d"),
    )
    class Meta:
        verbose_name = "coffee"
        ordering = ['name']

    def __str__(self):
        return self.name


class Opinion(models.Model):
    """
    Basic class for Opinion
    """

    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    rating = models.FloatField(
        default=0.0, help_text="Enter coffee rating in scale 0-10"
    )
    opinion = models.TextField(
        blank=True, help_text="Describe your impressions with this coffee"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acidity = models.IntegerField(default=0)
    body = models.IntegerField(default=0)
    flavor = models.IntegerField(default=0)
    bitterness = models.IntegerField(default=0)

class UserCoffee(models.Model):
    """
    Model for storing user coffee info (ex. add date, rating, opinion etc.)
    """

    # Foreign key used because User can only add one instance of each copy to history
    # But coffee can be in many other Users history
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    add_date = models.DateField(
        default=timezone.now().strftime("%Y-%m-%d")
    )
    opinion = models.OneToOneField(Opinion, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-add_date"]

    def __str__(self):
        return self.coffee.name

