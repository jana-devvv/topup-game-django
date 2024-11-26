from django.contrib import admin
from .models import Game, Package, Transaction, Payment

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'game', 'price')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'game_id')

@admin.register(Payment)
class Paymentadmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'method', 'is_verified', 'created_at')
    list_filter = ('method', 'is_verified')
