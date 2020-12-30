from django.contrib import admin
from .models import CrystalData

# Register your models here.


class CrystalDataAdmin(admin.ModelAdmin):
    list_display = ('crystal_system', 'cell_lenght_a', 'cell_lenght_b',
                    'cell_lenght_c','cell_angle_alpha', 'cell_angle_beta', 'cell_angle_gamma')


admin.site.register(CrystalData, CrystalDataAdmin)

