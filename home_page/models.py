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
    
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.item_name} - {self.created_at.date()}"
    
class FoundItem(models.Model):
    # STATUS_CHOICES = [
    #     ('pending', 'Pending'),
    #     ('claimed', 'Claimed'),
    #     ('returned', 'Returned')
    # ]

    CATEGORY_CHOICES = [
        ('stationery', 'Stationery'),
        ('notebooks', 'Notebooks / Textbooks'),
        ('bags', 'Bags / Backpacks'),
        ('clothing', 'Clothing (Jackets, Hoodies, Uniforms)'),
        ('footwear', 'Footwear'),
        ('water_bottle', 'Water Bottles'),
        ('lunch_box', 'Lunch Boxes'),
        ('eyeglasses', 'Eyeglasses'),
        ('electronics', 'Electronics'),
        ('sports_equipment', 'Sports Equipment'),
        ('art_supplies', 'Art Supplies'),
        ('accessories', 'Accessories (Watches, Jewelry)'),
        ('id_cards', 'ID Cards / Bus Passes'),
    ]

    # Item Information
    image = models.ImageField(upload_to='found_items/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    item_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200)
    date_found = models.DateField()
    time_found = models.TimeField()
    description = models.TextField(blank=True)

    # Finder Information
    finder_name = models.CharField(max_length=100)
    finder_email = models.EmailField()
    finder_phone = models.CharField(max_length=15, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    # ml_confidence = models.FloatField(default=0.0)  # Store ML prediction confidence

    def __str__(self):
        return f"{self.category} - Found by {self.finder_name}"
    
class MatchedItem(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='matched_lost_items')
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name='matched_found_items')
    matched_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the match was made
    matched_by = models.CharField(max_length=100, blank=True)  # Name of the admin or system that made the match
    confidence_score = models.FloatField(default=0.0)  # Confidence score for the match (if applicable)

    def __str__(self):
        return f"Match: {self.lost_item.item_name} with {self.found_item.item_name}"