from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RVM, Deposit


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'total_points', 'total_weight_recycled']
    list_filter = ['is_active', 'date_joined']
    readonly_fields = ['total_points', 'total_weight_recycled']


@admin.register(RVM)
class RVMAdmin(admin.ModelAdmin):
    list_display = ['machine_id', 'location', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['machine_id', 'location']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['user', 'material_type', 'weight_kg', 'points_earned', 'deposited_at']
    list_filter = ['material_type', 'deposited_at']
    readonly_fields = ['points_earned']

