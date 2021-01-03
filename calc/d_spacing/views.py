# from django.shortcuts import render
import math
import decimal
from django.http import HttpResponse, request
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
    info = CrystalData.objects.get(id=4)
    context = {

        "object": info
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


def list_view(request):
    list_info = CrystalData.objects.all()
    context = {

        "object_list": list_info
    }
    return render(request, "crystal_list.html", context)


def get_d_result(crystal_structure, list_of_abc, list_of_hkl):
    h = list_of_hkl[0]
    k = list_of_hkl[1]
    l = list_of_hkl[2]

    a = float(list_of_abc[0])
    b = float(list_of_abc[1])
    c = float(list_of_abc[2])

    if crystal_structure == 'cubic':
        result = a/(math.sqrt((h ** 2) + (k ** 2) + (l ** 2)))
    if crystal_structure == 'hexagonal':
        result = (math.sqrt((4 / 3) * ((h ** 2) + (h * k) + (k ** 2)) / (a ** 2)) + math.sqrt((l ** 2) / (c ** 2))) ** -1
    if crystal_structure == 'orthormobic':
        (math.sqrt((h ** 2 / a ** 2) + (k ** 2 / b ** 2) + (l ** 2 / c ** 2))) ** -1
    if crystal_structure == 'tetragonal':
        return (math.sqrt((h ** 2 + k ** 2) / a ** 2) + (l ** 2 / c ** 2)) ** -1
    return round(result,4)


def hkl_crystal_view(request):
    info = CrystalData.objects.get(id=10)
    list_of_abc = [info.cell_lenght_a, info.cell_lenght_b, info.cell_lenght_c]
    crystal_structure= info.crystal_system
    h_range = [1, 2, 3, 4]
    k_range = [0, 1, 2, 3]
    l_range = [0, 1, 2, 3]

    list_of_results = []

    for h in h_range:
        for k in k_range:
            for l in l_range:
                result = get_d_result(crystal_structure, list_of_abc, [h, k, l])
                # cubic_result = info.cell_lenght_a/decimal.Decimal((math.sqrt((h ** 2) + (k ** 2) + (l ** 2))))
                # d_results(h,k,l)
                # list_of_results.append([h, k, l, cubic_result])
                list_of_results.append([h, k, l, result])

    context = {
        'crystal_name': info.crystal_name,
        'crystal_formula': info.crystal_formula,
        'crystal_system': info.crystal_system,
        'cell_lenght_a': info.cell_lenght_a,
        'cell_lenght_b': info.cell_lenght_b,
        'cell_lenght_c': info.cell_lenght_c,
        # 'cubic_result': cubic_result,
        'list_of_results': list_of_results
    }

    return render(request, "hkl_crystal.html", context)



# def cubic(request):

#     cubic_result = ('cell_lenght_a' / (math.sqrt((h ** 2) + (k ** 2) + (l ** 2))))

#     context = {
#         'cubic_result' : cubic_result,

#     }

#     return render(request, "", context)


# cubic_result = (a / (math.sqrt((h ** 2) + (k ** 2) + (l ** 2))))
