from django.db import models



class Division(models.Model):
    name = models.CharField(max_length=255, default="Unknown")


class Department(models.Model):
    name = models.CharField(max_length=255, default="Unknown") 
    
class ProductClass(models.Model):
    name = models.CharField(max_length=255, default="Unknown")




class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐☆☆☆☆'),
        (2, '⭐⭐☆☆☆'),
        (3, '⭐⭐⭐☆☆'),
        (4, '⭐⭐⭐⭐☆'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(unique=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True,
    blank=True)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True,
    blank=True)  
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, null=True,
    blank=True) 
    
  
  
    class Meta: 
        pass

    def __str__(self):
        return self.title if self.title else f"Review {self.id}"