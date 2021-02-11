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
        #     'cell_length_a',
        #     'cell_length_b',
        #     'cell_length_c',
        #     'cell_angle_alpha',
        #     'cell_angle_beta',
        #     'cell_angle_gamma'
        # ]
