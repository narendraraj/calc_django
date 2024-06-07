from django.contrib import admin
from .models import CrystalData


# Register your models here.

class CrystalDataAdmin(admin.ModelAdmin):
    list_display = (
        'crystal_formula', 'crystal_system', 'crystal_name', 'cell_length_a', 'cell_length_b',
        'cell_length_c', 'cell_angle_alpha', 'cell_angle_beta', 'cell_angle_gamma', 'cif_file'
    )


admin.site.register(CrystalData, CrystalDataAdmin)

