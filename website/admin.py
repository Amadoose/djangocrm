# admin.py
from django.contrib import admin
from .models import Cliente, Hotel, Airline, Activity, Operator, Transport

# Register Cliente model (assuming it exists)
admin.site.register(Cliente)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price_per_night', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('name', 'location', 'contact_email')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'is_active', 'created_at')
    list_filter = ('country', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'country')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'duration', 'price', 'created_at')
    list_filter = ('type', 'location', 'created_at')
    search_fields = ('name', 'location', 'supplier')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'is_active', 'created_at')
    list_filter = ('type', 'location', 'is_active', 'created_at')
    search_fields = ('name', 'location', 'contact_email')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'capacity', 'price_per_unit', 'is_active', 'created_at')
    list_filter = ('type', 'location', 'is_active', 'created_at')
    search_fields = ('name', 'location', 'contact_email')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)