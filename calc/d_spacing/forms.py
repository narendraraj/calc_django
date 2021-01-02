from django import forms

from .models import CrystalData


class CrystalDataForm(forms.ModelForm):
    class Meta:
        model = CrystalData
        fields = '__all__'
        # fields = [
        #     'crytal_formula',
        #     'crystal_name',
        #     'crystal_system',
        #     'cell_lenght_a',
        #     'cell_lenght_b',
        #     'cell_lenght_c',
        #     'cell_angle_alpha',
        #     'cell_angle_beta',
        #     'cell_angle_gamma'
        # ]
