from django import forms
from django.forms import ClearableFileInput
from django.core.exceptions import ValidationError

from .models import CrystalData


class CrystalDataForm(forms.ModelForm):
    class Meta:
        model = CrystalData
        fields = "__all__"
        # fields = [
        #     'crystal_formula',
        #     'crystal_name',
        #     'crystal_system',
        #     'cell_length_a',
        #     'cell_length_b',
        #     'cell_length_c',
        #     'cell_angle_alpha',
        #     'cell_angle_beta',
        #     'cell_angle_gamma',
        # 'cif_file',

        # ]


# class CifCrystalDataForm(forms.ModelForm):
#     class Meta:
#         model = CrystalData
#         fields = '__all__'
#         fields = [
#         #     'crystal_formula',
#         #     'crystal_name',
#         #     'crystal_system',
#         #     'cell_length_a',
#         #     'cell_length_b',
#         #     'cell_length_c',
#         #     'cell_angle_alpha',
#         #     'cell_angle_beta',
#         #     'cell_angle_gamma',
#             'cif_file',

#         ]
#         widgets = {'cif_file': ClearableFileInput(attrs={'multiple': True})
#         }


class CifCrystalDataForm(forms.ModelForm):
    class Meta:
        model = CrystalData
        fields = ["cif_file"]
        widgets = {"cif_file": ClearableFileInput(attrs={"multiple": True})}

    def clean_cif_file(self):
        file = self.cleaned_data.get('cif_file')
        if file:
            extension = file.name.split('.')[-1].lower()
            if extension != 'cif':
                raise ValidationError("Only CIF files are allowed.")
        return file
