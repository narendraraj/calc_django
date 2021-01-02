# from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

from .models import CrystalData
from .forms import CrystalDataForm

# Create your views here.


def crystal_data_create_view(request):
    form = CrystalDataForm(request.POST or None)
    if form.is_valid():
        form.save()
        # print(form)
        form = CrystalDataForm()

    context = {

        'form': form
    }
    return render(request, "crystal_data_create.html", context)


# def home_view(request*args, **kwargs):

def home_view(request):
    # print(args, kwargs)
    # print(request.user)
    info = CrystalData.objects.get(id=5)
    context = {

        'object': info
    }
    return render(request, "home.html", context)
    # context = {
    #     'crystal_system': info.crystal_system,
    #     'cell_lenght_a': info.cell_lenght_a,
    #     'cell_lenght_b': info.cell_lenght_b,
    #     'cell_lenght_c': info.cell_lenght_c,
    #     'cell_angle_alpha': info.cell_angle_alpha,
    #     'cell_angle_beta': info.cell_angle_beta,
    #     'cell_angle_gamma': info.cell_angle_gamma
    # }


# def crystal_data_view(request):
#     info = CrystalData.objects.get(id=1)
#     context = {
#         'crystal_system': info.crystal_system,
#         'cell_lenght_a': info.cell_lenght_a,
#         'cell_lenght_b': info.cell_lenght_b,
#         'cell_lenght_c': info.cell_lenght_c,


#     }

#     return render(request, "home.html", context)
