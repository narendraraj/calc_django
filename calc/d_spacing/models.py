from django.db import models
from django.urls import reverse


# # Create your models here.


class CrystalData(models.Model):
    crystal_formula = models.CharField(max_length=25, blank=True, null=True)
    crystal_name = models.CharField(max_length=125, blank=True,  null=True)
    crystal_system = models.CharField(max_length=25, blank=True, null=True )
    cell_length_a = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    cell_length_b = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    cell_length_c = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    cell_angle_alpha = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cell_angle_beta = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cell_angle_gamma = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    space_group_name = models.CharField(max_length=25, null = True, blank= True)
    space_group_IT_number = models.IntegerField(null = True, blank = True)
    cif_file = models.FileField(upload_to= 'cif_database', blank= False, null= False)
    file_url = models.URLField(max_length=200, blank=True, null=True)
    comments = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True, auto_now_add=False)
    activate = models.BooleanField(default=False)

    

    # class Meta:
    #   unique_together = ['cell_length_a', 'cell_length_c', 'cell_length_c']  
    def __str__(self):
        return self.crystal_formula
    
    def __str__(self):
        return self.crystal_name
    
    def __str__(self):
        return self.crystal_system
    
    def __str__(self):
        return self.space_group_name

    def __str__(self):
        return self.comments
    
    
    
    def delete(self, *args, **kwargs):
        self.cif_file.delete()
        super().delete(*args, **kwargs)
        
    class Meta:
        ordering = ['-created']
        # verbose_name_plural = 'dates'
        
    def get_absolute_url(self):
       return reverse('d_spacing:detail', args=[self.id])
 
