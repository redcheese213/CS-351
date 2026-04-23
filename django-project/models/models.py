from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=60)
    phoneNumber = models.CharField(max_length=10)

    class CustomerType(models.TextChoices):
        PURCHASE = 'Purchase',
        SERVICE = 'Service',
        VISIT = 'Visit',

    customerType = models.CharField(
        max_length=8,
        choices=CustomerType.choices,
        default=CustomerType.SERVICE,
    )


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=10)


class Vehicle(models.Model):
    make = models.CharField(max_length=60)
    model = models.CharField(max_length=60)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class VehicleStatus(models.TextChoices):
        INVENTORY = 'Inventory'
        SOLD = 'Sold'
        IN_SERVICE = 'In-Service'

    status = models.CharField(
        max_length=10,
        choices=VehicleStatus.choices,
        default=VehicleStatus.INVENTORY,
    )


class Billing(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class PaymentMethod(models.TextChoices):
        CASH = 'Cash'
        CREDIT = 'Credit'
        DEBIT = 'Debit'
        FINANCING = 'Financing'
        CHECK = 'Check'

    paymentMethod = models.CharField(
        max_length=9,
        choices=PaymentMethod.choices,
    )


class Sales(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.PROTECT) # uses OneToOneField since a vehicle should only ever be sold once.
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    dateSold = models.DateField()
    tagNumber = models.CharField(max_length=20, unique=True)
    customizations = models.TextField(blank=True)
    billing = models.ForeignKey(Billing, on_delete=models.PROTECT)


class ServiceData(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    arrivalMileage = models.IntegerField()
    departureMileage = models.IntegerField()
    estimate = models.DecimalField(max_digits=10, decimal_places=2)
    billing = models.ForeignKey(Billing, on_delete=models.PROTECT)
    note = models.TextField(blank=True)


class WorkedOn(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    serviceData = models.ForeignKey(ServiceData, on_delete=models.PROTECT)
    hours = models.DecimalField(max_digits=5, decimal_places=2)


class InventoryVehicle(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.PROTECT) # uses OneToOneField since a vehicle should only ever be sold once.

    class Location(models.TextChoices):
        MAIN_LOT = 'Main Lot'
        REMOTE_LOT = 'Remote Lot'
        OTHER_DEALERSHIP = 'Other Dealership'
        IN_TRANSIT = 'In Transit'

    location = models.CharField(
        max_length=17,
        choices=Location.choices,
        default=Location.MAIN_LOT,
    )
    note = models.TextField(blank=True)


# when an inventoryVehicle is created, set the corresponding to be in inventory
@receiver(post_save, sender=InventoryVehicle)
def sync_vehicle_status_on_save(sender, instance, **kwargs):
    instance.vehicle.status = Vehicle.VehicleStatus.INVENTORY
    instance.vehicle.save()

# likewise for when an inventory vehicle is created
@receiver(post_delete, sender=InventoryVehicle)
def sync_vehicle_status_on_delete(sender, instance, **kwargs):
    instance.vehicle.status = Vehicle.VehicleStatus.IN_SERVICE
    instance.vehicle.save()

# when a sales record is created, set the corresponding vehicle to sold
@receiver(post_save, sender=Sales)
def sync_vehicle_status_on_sale(sender, instance, **kwargs):
    instance.vehicle.status = Vehicle.VehicleStatus.SOLD
    instance.vehicle.save()
