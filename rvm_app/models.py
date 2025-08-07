from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

# model user use AbstractUser
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    total_points = models.PositiveIntegerField(default=0)
    total_weight_recycled = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def add_points(self, points):
        """Safely add points to user's total"""
        self.total_points += points
        self.save(update_fields=['total_points'])
    
    def add_weight(self, weight):
        """Add recycled weight to user's total"""
        self.total_weight_recycled += Decimal(str(weight))
        self.save(update_fields=['total_weight_recycled'])

# the machines model 
class RVM(models.Model):
    machine_id = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"RVM-{self.machine_id} at {self.location}"

#Material types with point values
class MaterialType(models.TextChoices):
    PLASTIC = 'plastic', 'Plastic'
    METAL = 'metal', 'Metal'
    GLASS = 'glass', 'Glass'

#Individual deposit transaction
class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    rvm = models.ForeignKey(RVM, on_delete=models.CASCADE, related_name='deposits')
    material_type = models.CharField(max_length=10, choices=MaterialType.choices, default=MaterialType.PLASTIC)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2)
    points_earned = models.PositiveIntegerField()
    deposited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-deposited_at']
    
    def save(self, *args, **kwargs):
        """Auto-calculate points before saving"""
        if not self.points_earned:
            self.points_earned = self.calculate_points()
        super().save(*args, **kwargs)
        
        # Update user totals
        self.user.add_points(self.points_earned)
        self.user.add_weight(self.weight_kg)
    
    def calculate_points(self):
        """Calculate reward points based on material type and weight"""
        point_rates = {
            MaterialType.PLASTIC: 1,  # 1 point/kg
            MaterialType.METAL: 3,    # 3 points/kg
            MaterialType.GLASS: 2,    # 2 points/kg
        }
        rate = point_rates.get(self.material_type, 0)
        return int(float(self.weight_kg) * rate)
