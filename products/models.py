from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    harvest_date = models.DateField()
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name