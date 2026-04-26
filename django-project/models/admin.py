from django.contrib import admin
from django.db.models.fields.related import ForeignObjectRel
from djangoql.admin import DjangoQLSearchMixin
from .models import (
    Customer, Employee, Vehicle, Billing,
    Sales, ServiceData, WorkedOn, InventoryVehicle
)

from import_export.admin import ImportExportModelAdmin

def get_fields(model):
    return [
        field.name for field in model._meta.get_fields()
        if not isinstance(field, ForeignObjectRel)
    ]

@admin.register(Customer)
class CustomerAdmin(DjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = get_fields(Customer)

@admin.register(Employee)
class EmployeeAdmin(DjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = get_fields(Employee)

@admin.register(Vehicle)
class VehicleAdmin(DjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = get_fields(Vehicle)

@admin.register(Billing)
class BillingAdmin(DjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin):
    search_field = ('customer__name')
    list_display = get_fields(Billing)
# Your desired filters
    list_filter = ('paymentMethod', 'date')

    
@admin.register(Sales)
class SalesAdmin(DjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = get_fields(Sales)

@admin.register(ServiceData)
class ServiceDataAdmin(DjangoQLSearchMixin, ImportExportModelAdmin,  admin.ModelAdmin):
    list_display = get_fields(ServiceData)

@admin.register(WorkedOn)
class WorkedOnAdmin(DjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = get_fields(WorkedOn)

@admin.register(InventoryVehicle)
class InventoryVehicleAdmin(DjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = get_fields(InventoryVehicle)