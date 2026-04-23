from django.contrib import admin
from django.db.models.fields.related import ForeignObjectRel
from djangoql.admin import DjangoQLSearchMixin
from .models import (
    Customer, Employee, Vehicle, Billing,
    Sales, ServiceData, WorkedOn, InventoryVehicle
)

def get_fields(model):
    return [
        field.name for field in model._meta.get_fields()
        if not isinstance(field, ForeignObjectRel)
    ]

@admin.register(Customer)
class CustomerAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(Customer)

@admin.register(Employee)
class EmployeeAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(Employee)

@admin.register(Vehicle)
class VehicleAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(Vehicle)

@admin.register(Billing)
class BillingAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(Billing)

@admin.register(Sales)
class SalesAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(Sales)

@admin.register(ServiceData)
class ServiceDataAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(ServiceData)

@admin.register(WorkedOn)
class WorkedOnAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(WorkedOn)

@admin.register(InventoryVehicle)
class InventoryVehicleAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = get_fields(InventoryVehicle)