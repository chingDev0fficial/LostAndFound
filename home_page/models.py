from django.db import models

# Create your models here.
class LostItem(models.Model):
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    date_lost = models.DateField()
    time_lost = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items/', null=True, blank=True)
    
    # Contact Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    preferred_contact = models.CharField(max_length=10)
    
    # Additional Verification
    # proof_of_ownership = models.FileField(upload_to='proofs/', null=True, blank=True)
    # reference_number = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.item_name} - {self.created_at.date()}"