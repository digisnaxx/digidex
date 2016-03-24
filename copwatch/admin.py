from django.contrib import admin

from models import *


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date')
    list_filter = ('date',)
    prepopulated_fields = {"slug": ("subject",)}

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('car_num', 'car_make', 'car_model', 'car_year')


class VehicleInline(admin.StackedInline):
    model = Vehicle.officers.through
    extra = 1


class OfficerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'precinct',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [VehicleInline,]
    exclude = ('unit', 'division', )


class DivisionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class UnitAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Officer, OfficerAdmin)
admin.site.register(Precinct)
admin.site.register(Bureau)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Unit, UnitAdmin)
