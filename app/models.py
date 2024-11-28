from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Package(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.game.name}"
    
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='transactions')
    player_id = models.CharField(max_length=50) # ID in game player
    server_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username}"
    
class Payment(models.Model):    
    METHOD_CHOICES = [
        ('gopay', 'GoPay'),
        ('dana', 'Dana'),
        ('ovo', 'OVO'),
        ('shopeepay', 'ShopeePay'),
    ]

    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='dana')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction.id} - {self.status}"