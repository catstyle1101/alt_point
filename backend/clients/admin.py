from django.contrib import admin

from clients import models as m


@admin.register(m.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'typeEducation', 'dob', 'monIncome')
    list_filter = ('typeEducation', 'dob', 'spouse')
    search_fields = ('name', 'surname')


@admin.register(m.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'zipCode', 'country', 'city', 'street', 'house', 'apartment')
    list_filter = ('country', 'city')


@admin.register(m.Passport)
class PassportAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Communication)
class CommunicationAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'dob')
