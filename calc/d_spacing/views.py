# from django.shortcuts import render
import math
# import decimal
from django.http import HttpResponse, request, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import CrystalData
from .forms import CrystalDataForm
from django.template.defaultfilters import lower

# Create your views here.

# pulled object from database for testing purpose as global varibale 'info'
# info = CrystalData.objects.get(id=10)
def database_search_view(request):
    
    query = request.GET.get('q') # this is a dictionary
    
    qs = CrystalData.objects.all()
    if query is not None:
        lookups =Q(id__icontains = query) | Q(crystal_formula__icontains = query) | Q(crystal_name__icontains=query) | Q(crystal_system__icontains=query)
        qs = CrystalData.objects.filter(lookups)
          
    
    context = {
        "object_list": qs
        
    }
    
    return render(request, "database_search.html", context )

def home_view(request):
    # print(args, kwargs)
    # print(request.user)
    # info = CrystalData.objects.get(id=1)

    context = {

        "object": ""
    }
    return render(request, "home.html", context)

    # context = {
    #     'crystal_system': info.crystal_system,
    #     'cell_length_a': info.cell_length_a,
    #     'cell_length_b': info.cell_length_b,
    #     'cell_length_c': info.cell_length_c,
    #     'cell_angle_alpha': info.cell_angle_alpha,
    #     'cell_angle_beta': info.cell_angle_beta,
    #     'cell_angle_gamma': info.cell_angle_gamma
    # }


def crystal_data_create_view(request):
    """

    A view to create the form for to input crystal (materials) structure infroamtion and saves it to the database.    
    class CryatalDataForm is called from forms.py.
    This function uses POST method.

    """

    form = CrystalDataForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CrystalDataForm()

    context = {

        'form': form
    }
    return render(request, "crystal_data_create.html", context)


def update_crystal_data_view(request, crystal_id):
    # print(args, kwargs)
    # print(request.user)
    info_update = CrystalData.objects.get(id= crystal_id)
    form = CrystalDataForm(instance=info_update)

    if request.method == 'POST':
        form = CrystalDataForm(request.POST, instance= info_update)
        if form.is_valid():
            form.save()
           
            return  redirect('/database/')

    context = {

        'form': form,
        'crystal_id': crystal_id

    }

    return render(request, 'update_crystal_data.html', context)


# def update_crystal_data_view(request, crystal_id):
#     # print(args, kwargs)
#     # print(request.user)
#     info_delete = CrystalData.objects.get(id=crystal_id)
#     form = CrystalDataForm(instance=info_delete)

#     if request.method == 'POST':
#         # print('Printing POST:', request.POST)
#         form = CrystalDataForm(request.POST, instance=info_delete)
#         if form.is_valid():
#             form.save()            
#             return redirect('/database/')

#     context = {

#         'form': form,
#         'crystal_id': crystal_id


#     }

#     return render(request, 'update_crystal_data.html', context)


# def update_crystal_data_view(request, update_id):
#     # print(args, kwargs)
#     # print(request.user)
#     update = CrystalData.objects.get(id= update_id)
#     form = CrystalDataForm(instance=update)

#     if request.method == 'POST':
#         form = CrystalDataForm(request.POST, instance= update)
#         if form.is_valid():
#             form.save()
#             form = CrystalDataForm()
#             # return redirect('database/')

#     context = {

#         'form' : form


#     }


#     return render(request, 'update_crystal_data.html', context)


def delete_crystal_data_view(request,crystal_id ):    
    crystal_object = get_object_or_404(CrystalData, id=crystal_id)
    # form = CrystalDataForm(request.POST,instance=info )

    if crystal_object:
        crystal_object.delete()
    return redirect('/database/')
    
       

def list_view(request):
    info = CrystalData.objects.all()
    context = {

        "object_list": info
    }
    return render(request, "crystal_list.html", context)


def database_view(request):
    info = CrystalData.objects.all()
    context = {

        "object_list": info
    }
    return render(request, "database_view.html", context)


def get_d_result(crystal_structure, list_of_abc, list_of_hkl):
    h = list_of_hkl[0]
    k = list_of_hkl[1]
    l = list_of_hkl[2]

    a = float(list_of_abc[0])
    b = float(list_of_abc[1])
    c = float(list_of_abc[2])

    if lower(crystal_structure) == 'cubic':
        d_result = a/(math.sqrt((h ** 2) + (k ** 2) + (l ** 2)))
    if lower(crystal_structure) == 'hexagonal':
        d_result = (math.sqrt((4 / 3) * ((h ** 2) + (h * k) + (k ** 2)
                                       ) / (a ** 2)) + math.sqrt((l ** 2) / (c ** 2))) ** -1
    if lower(crystal_structure) == 'orthorhombic':
        d_result = (math.sqrt((h ** 2 / a ** 2) +
                            (k ** 2 / b ** 2) + (l ** 2 / c ** 2))) ** -1
    # if lower(crystal_structure) == 'tetragonal':
    #     d_result = (math.sqrt((h ** 2 + k ** 2) / a ** 2) +
    #               (l ** 2 / c ** 2)) ** -1
    if lower(crystal_structure) == 'tetragonal':
        d_result = math.sqrt(((h ** 2 + k ** 2 + l**2*(a/c)**2))*(1/ a ** 2))** -1
    return round(d_result, 4)




def result_hkl_view_by_id(request, crystal_id):
    # info = CrystalData.objects.get(id=id)
    info = get_object_or_404(CrystalData, id=crystal_id)
    # info = get_object_or_404(CrystalData, crystal_formula=crystal_formula)
    list_of_abc = [info.cell_length_a, info.cell_length_b, info.cell_length_c]
    crystal_structure = info.crystal_system
    h_range = range(1, 3)
    k_range = range(0, 4)
    l_range = range(0, 4)

    list_of_results = []

    # for h in h_range:
    for h in h_range:
        for k in k_range:
            for l in l_range:
                result = get_d_result(
                    crystal_structure, list_of_abc, [h, k, l])
                # cubic_result = info.cell_length_a/decimal.Decimal((math.sqrt((h ** 2) + (k ** 2) + (l ** 2))))
                # d_results(h,k,l)
                # list_of_results.append([h, k, l, cubic_result])
                list_of_results.append([h, k, l, result])

    context = {
        'crystal_id': crystal_id,
        'crystal_name': info.crystal_name,
        'crystal_formula': info.crystal_formula,
        'crystal_system': info.crystal_system,
        'cell_length_a': info.cell_length_a,
        'cell_length_b': info.cell_length_b,
        'cell_length_c': info.cell_length_c,
        'cell_angle_alpha': info.cell_angle_alpha,
        'cell_angle_beta': info.cell_angle_beta,
        'cell_angle_gamma': info.cell_angle_gamma,
        'list_of_results': list_of_results
    }

    return render(request, "result_hkl_view_by_id.html", context)


def hkl_crystal_view(request):
    info = CrystalData.objects.get(id=1)  # for specific id
    list_of_abc = [info.cell_length_a, info.cell_length_b, info.cell_length_c]
    crystal_structure = info.crystal_system
    h_range = [1, 2, 3]
    k_range = [0, 1, 2, 3]
    l_range = [0, 1, 2, 3]

    list_of_results = []

    for h in h_range:
        for k in k_range:
            for l in l_range:
                result = get_d_result(
                    crystal_structure, list_of_abc, [h, k, l])
                # cubic_result = info.cell_length_a/decimal.Decimal((math.sqrt((h ** 2) + (k ** 2) + (l ** 2))))
                # d_results(h,k,l)
                # list_of_results.append([h, k, l, cubic_result])
                list_of_results.append([h, k, l, result])

    context = {
        'crystal_name': info.crystal_name,
        'crystal_formula': info.crystal_formula,
        'crystal_system': info.crystal_system,
        'cell_length_a': info.cell_length_a,
        'cell_length_b': info.cell_length_b,
        'cell_length_c': info.cell_length_c,
        'cell_angle_alpha': info.cell_angle_alpha,
        'cell_angle_beta': info.cell_angle_beta,
        'cell_angle_gamma': info.cell_angle_gamma,
        # 'cubic_result': cubic_result,
        'list_of_results': list_of_results
    }

    return render(request, "hkl_crystal.html", context)
