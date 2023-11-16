from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

# Create your views here.
MyUser = get_user_model()

# # Create your models here.


class CrystalData(models.Model):
    crystal_formula = models.CharField(max_length=125, blank=True, null=True)
    crystal_name = models.CharField(max_length=125, blank=True, null=True)
    crystal_system = models.CharField(max_length=125, blank=True, null=True)
    cell_length_a = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True
    )
    cell_length_b = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True
    )
    cell_length_c = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True
    )
    cell_angle_alpha = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    cell_angle_beta = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    cell_angle_gamma = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    space_group_name = models.CharField(max_length=125, null=True, blank=True)
    space_group_it_number = models.IntegerField(null=True, blank=True)
    symmetry_space_group_name_H_M = models.CharField(
        max_length=225, blank=True, null=True
    )
    cif_file = models.FileField(upload_to="cif_database", blank=False, null=False)
    file_url = models.URLField(max_length=200, blank=True, null=True)
    comments = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    activate = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, null=True, blank=True
    )

    # class Meta:
    #   unique_together = ['cell_length_a', 'cell_length_c', 'cell_length_c']

    def __str__(self):
        return str(self.crystal_formula)

    def __str__(self):
        return str(self.crystal_name)

    def __str__(self):
        return str(self.crystal_system)

    def __str__(self):
        return str(self.space_group_name)

    def __str__(self):
        return str(self.comments)

    # def uploaded_by_first_name(self):
    #     if self.uploaded_by:
    #         return self.uploaded_by.first_name
    #     else:
    #         return ""

    def delete(self, *args, **kwargs):
        self.cif_file.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        # verbose_name_plural = 'dates'

    def get_absolute_url(self):
        return reverse("d_spacing:detail", args=[self.id])

    # def get_download_url(self):
    #     return reverse_lazy("download_cif_file", args=[self.id])
