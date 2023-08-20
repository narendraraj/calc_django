# from django.shortcuts import render
from inspect import unwrap
import json
import os
import math
from time import time
from poplib import CR
from pyexpat.errors import messages
import re
from urllib import response
from venv import create
# import decimal
from django.http import HttpResponse, request, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


from .models import CrystalData
from .forms import CrystalDataForm, CifCrystalDataForm
from . import readcif


from django.template.defaultfilters import lower

from gemmi import cif
import requests
import itertools

from django.conf import settings
import Dans_Diffraction as dif

from .calculator_dspacing import CrystalAnalyzer
# Create your views here.


def home_view(request):

    # url = "http://stem-f2:851/"

    # method = {
    #     "jsonrpc": "2.0",
    #     "method": "computer.info",
    #     "id" : 14
    # }
    # request_body = json.dumps(method, indent=4)
    # response1 = requests.post(url,  headers={'Content-Type': 'application/json'}, data=request_body)
    # print(response1.json())
    # # print('uptime is:', response.json()['result']['info']['up_time'])

    # # print(type(ram_total)

    # ram_total = response1.json()['result']['info']['ram_total']
    # ram_total_gb = int(ram_total)*1e-9

    # method2 = {
    #     "jsonrpc": "2.0",
    #     "method": "highVoltage.hv100.voltage.getMeasured",
    #     "id" : 115

    # }
    # request_body = json.dumps(method2, indent=4)
    # response2 = requests.post(url, headers={'Content-Type': 'application/json'}, data=request_body)
    # print(response2.json())

    # high_voltatage = response2.json()['result']['voltage']

    context = {

        # "object": "",
        # "response": response,
        # "ram_total_gb": ram_total_gb,
        # "high_voltatage" : high_voltatage,
    }
    return render(request, "d_spacing/home.html", context)

    # context = {
    #     'crystal_system': info.crystal_system,
    #     'cell_length_a': info.cell_length_a,
    #     'cell_length_b': info.cell_length_b,
    #     'cell_length_c': info.cell_length_c,
    #     'cell_angle_alpha': info.cell_angle_alpha,
    #     'cell_angle_beta': info.cell_angle_beta,
    #     'cell_angle_gamma': info.cell_angle_gamma
    # }


def database_list_view(request, page=1):

    query = ""

    query = request.GET.get('q', '')  # this is a dictionary

    if query is not None:
        lookups = Q(id__icontains=query) | Q(crystal_formula__icontains=query) | Q(
            crystal_name__icontains=query) | Q(crystal_system__icontains=query)
        qs = CrystalData.objects.filter(lookups)

    # Pagination
    page = request.GET.get('page', 1)
    qs_paginator = Paginator(qs, 15)
    total_object = qs_paginator.count

    try:
        qs = qs_paginator.page(page)

    except PageNotAnInteger:
        qs = qs_paginator.page(1)
    except EmptyPage:
        qs = qs_paginator.page(qs_paginator.num_pages)

    context = {
        "object_list": qs,
        "total_object":  total_object,

    }
    return render(request, "d_spacing/database_list.html", context)


def crystal_data_create_view(request):
    """

    A view to create the form for to input crystal (materials) structure infroamtion and saves it to the database.
    class CryatalDataForm is called from forms.py.
    This function uses POST method.

    """
    form = CrystalDataForm(request.FILES)
    if request.method == 'POST':
        form = CrystalDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('d_spacing:database_list'))

    context = {

        'form': form
    }
    return render(request, "d_spacing/crystal_data_create.html", context)


def update_crystal_data_view(request, crystal_id):
    # print(args, kwargs)
    # print(request.user)
    info_update = CrystalData.objects.get(id=crystal_id)
    form = CrystalDataForm(instance=info_update)

    if request.method == 'POST':
        form = CrystalDataForm(request.POST or None,
                               request.FILES or None, instance=info_update)
        if form.is_valid():
            form.save()
            messages.success(request, "Material data successfuly updated ")
            return redirect(reverse('d_spacing:database_list'))

    context = {

        'form': form,
        'crystal_id': crystal_id

    }

    return render(request, 'd_spacing/update_crystal_data.html', context)


def delete_crystal_data_view(request, crystal_id):
    crystal_object = get_object_or_404(CrystalData, id=crystal_id)
    if request. method == "POST":
        crystal_object.delete()
        messages.success(request, "Material data successfuly deleted ")
        return redirect(reverse('d_spacing:database_list'))

    context = {

        "object": crystal_object
    }
    return render(request, "d_spacing/delete_crystal_data.html", context)




def dspacing_results_view(request, crystal_id):
    # info = CrystalData.objects.get(id=id)
    info = get_object_or_404(CrystalData, id=crystal_id)
    # info = get_object_or_404(CrystalData, crystal_formula=crystal_formula)
    unit_cell_length_a = float(info.cell_length_a)
    unit_cell_length_b = float(info.cell_length_b)
    unit_cell_length_c = float(info.cell_length_c)
    unit_cell_angle_alpha = float(info.cell_angle_alpha)
    unit_cell_angle_beta = float(info.cell_angle_beta)
    unit_cell_angle_gamma = float(info.cell_angle_gamma)

    analyzer = CrystalAnalyzer(unit_cell_length_a, unit_cell_length_b,  unit_cell_length_c, unit_cell_angle_alpha, unit_cell_angle_beta,unit_cell_angle_gamma)

    crystal_system = info.crystal_system
    print(crystal_system)

    if crystal_system == "None":
        crystal_system = f"{analyzer.structure} - (calculated, No value found in CIF)"
        print(crystal_system)

    miller_index_results = []

    for miller_index_h in range(1, 3):
        for miller_index_k in range(0, 4):
            for miller_index_l in range(0, 4):
                d_spacing = analyzer.calculate_d_spacing(miller_index_h, miller_index_k, miller_index_l).__round__(4)
                miller_index_results.append((miller_index_h, miller_index_k, miller_index_l, d_spacing))
    print(f"The determined crystal structure is: {analyzer.structure}")
    print("Miller Index (hkl) - D-spacing results:")
    for result in miller_index_results:
        print(f"({result[0]}, {result[1]}, {result[2]}) - {result[3]:.4f} Å")

    context = {

        'crystal_id': crystal_id,
        'crystal_name': info.crystal_name,
        'crystal_formula': info.crystal_formula,
        'crystal_system':  crystal_system,
        'cell_length_a': info.cell_length_a,
        'cell_length_b': info.cell_length_b,
        'cell_length_c': info.cell_length_c,
        'cell_angle_alpha': info.cell_angle_alpha,
        'cell_angle_beta': info.cell_angle_beta,
        'cell_angle_gamma': info.cell_angle_gamma,
        'list_of_results': miller_index_results

    }

    return render(request, "d_spacing/dspacing_results.html", context)






def upload_cif_file_view(request):
    if request.method == 'POST':
        form = CifCrystalDataForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist("cif_file")
        if form.is_valid():
            for file in files:
                file_instance = CrystalData.objects.create(cif_file=file)
                file_instance.save()

                file_path = file_instance.cif_file.path
                instance_id = file_instance.id

                # info = get_object_or_404(CrystalData, id=instance_id)

                # print(info.id)
                # print(info.cell_length_a)

                xtl = dif.Crystal(file_path)
                doc = cif.read_file(file_path)
                block = doc.sole_block()
                # a= xtl.Cell.a

                # print(file_path)
                # doc=readcif.readcif(file_path)
                # print(json.dumps(doc, indent=4))
                # print(doc["_cell_length_a"])
                # print(doc)
                # print(doc.values())
                # readcif.readcif()
                # print(a)

                CrystalData.objects.filter(id=instance_id).update(
                    crystal_name=str(block.find_value('_chemical_name_mineral') or block.find_value(
                        '_chemical_name_systematic')),
                    crystal_formula=str(
                        block.find_value('_chemical_formula_sum')),
                    cell_length_a=float(xtl.Cell.a),
                    # cell_length_a = doc["_cell_length_a"],
                    cell_length_b=float(xtl.Cell.b),
                    cell_length_c=float(xtl.Cell.c),
                    cell_angle_alpha=float(xtl.Cell.alpha),
                    cell_angle_beta=float(xtl.Cell.beta),
                    cell_angle_gamma=float(xtl.Cell.gamma),
                    space_group_IT_number=block.find_value(
                        '_space_group_IT_number') or block.find_value('_symmetry_Int_Tables_number'),
                    crystal_system=str(block.find_value('_symmetry_cell_setting') or block.find_value(
                        '_space_group_crystal_system'))),

                # doc= cif.read_file(file_path)
                # block = doc.sole_block()
                # CrystalData.objects.filter(id=instance_id).update(
                #     crystal_name = block.find_value('_chemical_name_mineral') or block.find_value('_chemical_name_systematic'),
                #     crystal_formula = block.find_value('_chemical_formula_sum'),
                #     crystal_system = block.find_value('_symmetry_cell_setting'),
                #     cell_length_a = block.find_value('_cell_length_a'),
                #     cell_length_b = block.find_value('_cell_length_b'),
                #     cell_length_c = block.find_value('_cell_length_c'),
                #     cell_angle_alpha = block.find_value('_cell_angle_alpha'),
                #     cell_angle_beta = block.find_value('_cell_angle_beta'),
                #     cell_angle_gamma =  block.find_value('_cell_angle_gamma')
                #     )

        messages.success(request, " CIF file is successfuly uploaded ")
        return redirect(reverse('d_spacing:database_list'))

    else:
        form = CifCrystalDataForm()

    context = {

        'form': form,

    }
    return render(request, "d_spacing/upload_cif_file.html", context)


# def read_latest_cif_file_updated_model():
#     latest_file_upload= CrystalData.objects.latest("id")
#     latest_file_upload_path = latest_file_upload.cif_file.path

#     doc = cif.read_file(latest_file_upload_path)
#     block = doc.sole_block()
#     c=CrystalData.objects.update(
#         crystal_name = block.find_value('_chemical_name_mineral') or block.find_value('_chemical_name_systematic'),
#         crystal_formula = block.find_value('_chemical_formula_sum'),
#         crystal_system = block.find_value('_symmetry_cell_setting'),
#         cell_length_a = block.find_value('_cell_length_a'),
#         cell_length_b = block.find_value('_cell_length_b'),
#         cell_length_c = block.find_value('_cell_length_c'),
#         cell_angle_alpha = block.find_value('_cell_angle_alpha'),
#         cell_angle_beta = block.find_value('_cell_angle_beta'),
#         cell_angle_gamma =  block.find_value('_cell_angle_gamma'),
#     )


# read_latest_cif_file_updated_model()


#     return render(request, "update_crystal_data.html")
# def read_file():
#     doc= read(file).decode("utf-8")
#     print(doc)


def cif_file_display_view(request, crystal_id):
    # info = CrystalData.objects.get(id=id)
    info = get_object_or_404(CrystalData, id=crystal_id)

    # imports data from model database
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
        'cif_file': info.cif_file,
        # 'cif_info' : cif_info,

    }

    return render(request, "d_spacing/cif_file_display.html", context)


# def list_view(request):
#     info = CrystalData.objects.all()
#     context = {

#         "object_list": info
#     }
#     return render(request, "crystal_list.html", context)


# def hkl_crystal_view(request):
#     info = CrystalData.objects.get(id=1)  # for specific id
#     list_of_abc = [info.cell_length_a, info.cell_length_b, info.cell_length_c]
#     crystal_structure = info.crystal_system
#     h_range = [1, 2, 3]
#     k_range = [0, 1, 2, 3]
#     l_range = [0, 1, 2, 3]

#     list_of_results = []

#     for h in h_range:
#         for k in k_range:
#             for l in l_range:
#                 result = get_d_result(
#                     crystal_structure, list_of_abc, [h, k, l])
#                 # cubic_result = info.cell_length_a/decimal.Decimal((math.sqrt((h ** 2) + (k ** 2) + (l ** 2))))
#                 # d_results(h,k,l)
#                 # list_of_results.append([h, k, l, cubic_result])
#                 list_of_results.append([h, k, l, result])

#     context = {
#         'crystal_name': info.crystal_name,
#         'crystal_formula': info.crystal_formula,
#         'crystal_system': info.crystal_system,
#         'cell_length_a': info.cell_length_a,
#         'cell_length_b': info.cell_length_b,
#         'cell_length_c': info.cell_length_c,
#         'cell_angle_alpha': info.cell_angle_alpha,
#         'cell_angle_beta': info.cell_angle_beta,
#         'cell_angle_gamma': info.cell_angle_gamma,
#         # 'cubic_result': cubic_result,
#         'list_of_results': list_of_results
#     }

#     return render(request, "hkl_crystal.html", context)
