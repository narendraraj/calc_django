from django.db import models


# # Create your models here.


class CrystalData(models.Model):
    crystal_formula = models.CharField(max_length=25, blank= True, null=True)
    crystal_name = models.CharField(max_length=125, blank= True, null=True)
    crystal_system = models.CharField(max_length = 25)
    cell_lenght_a = models.DecimalField(max_digits = 8, decimal_places = 4, blank = True, null = True)
    cell_lenght_b = models.DecimalField(max_digits = 8, decimal_places = 4, blank = True, null = True)
    cell_lenght_c = models.DecimalField(max_digits = 8, decimal_places = 4, blank = True, null = True)
    cell_angle_alpha = models.DecimalField(max_digits = 8, decimal_places = 2, blank = True, null = True)
    cell_angle_beta = models.DecimalField(max_digits = 8, decimal_places = 2, blank = True, null = True)
    cell_angle_gamma = models.DecimalField(max_digits = 8, decimal_places = 2, blank = True, null = True)

    # space_group_name = models.CharField(null = True, max_length=25)
    # space_group_IT_number   = models.IntegerField(null=True)

    def __str__(self):
        return self.crystal_system
