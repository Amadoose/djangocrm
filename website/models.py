from django.db import models

# Create your models here.


class Record(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the model was created")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)    

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")