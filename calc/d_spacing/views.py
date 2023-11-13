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
from django.http import JsonResponse
from django.http import HttpResponse, request, Http404
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import CrystalData, get_user_model
from .forms import CrystalDataForm, CifCrystalDataForm
from . import readcif
from .utils import parse_cif_file

# from account.forms import get_first_name_from_email, get_last_name_from_email

from django.template.defaultfilters import lower

from gemmi import cif
import requests
import itertools

from django.conf import settings
import Dans_Diffraction as dif

from .calculator_dspacing import CrystalAnalyzer


MyUser = get_user_model()
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


class CrystalDataListView(ListView):
    """
    A view that displays a list of CrystalData objects.

    Attributes:
        model: The model that the view will display.
        template_name: The name of the template to render.
        context_object_name: The name of the context variable to use in the template.
        paginate_by: The number of objects to display per page.

    Methods:
        get_queryset: Returns the queryset of objects to display.
    """

    model = CrystalData
    template_name = "d_spacing/database_list.html"
    context_object_name = "object_list"
    paginate_by = 20

    def get_queryset(self):
        """
        Returns the queryset of CrystalData objects to display.

        If a search query is provided in the request, filters the queryset to include only
        objects that match the query.

        Returns:
            A queryset of CrystalData objects.
        """
        query = self.request.GET.get("q", "")
        if query:
            return CrystalData.objects.filter(
                Q(id__icontains=query)
                | Q(crystal_formula__icontains=query)
                | Q(crystal_name__icontains=query)
                | Q(crystal_system__icontains=query)
            )
        return CrystalData.objects.all()


class CrystalDataUserListView(LoginRequiredMixin, ListView):
    """
    A view that displays a list of CrystalData objects uploaded by the current user.

    Attributes:
        model (CrystalData): The model that this view displays.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the context variable to use in the template.
        paginate_by (int): The number of objects to display per page.

    Methods:
        get_queryset(): Returns the queryset of CrystalData objects to display.
    """

    model = CrystalData
    template_name = "d_spacing/user_database_list.html"
    context_object_name = "object_list"
    paginate_by = 20

    def get_queryset(self):
        """
        Returns the queryset of CrystalData objects to display.

        If a search query is provided in the request, filters the queryset to include only
        objects that match the query and were uploaded by the current user. Otherwise, returns
        all objects uploaded by the current user.
        """
        query = self.request.GET.get("q", "")
        if query:
            return CrystalData.objects.filter(
                Q(id__icontains=query)
                | Q(crystal_formula__icontains=query)
                | Q(crystal_name__icontains=query)
                | Q(crystal_system__icontains=query),
                uploaded_by=self.request.user,
            )
        return CrystalData.objects.filter(uploaded_by=self.request.user)


class CrystalDataPaginator(Paginator):
    """
    A custom paginator class that extends Django's built-in Paginator class.
    This class adds functionality to handle exceptions when retrieving a page of data.
    """

    def __init__(
        self, request, object_list, per_page, orphans=0, allow_empty_first_page=True
    ):
        self.request = request
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)

    def get_page(self, number):
        try:
            return super().get_page(number)
        except Exception:
            return super().get_page(1)


def crystal_data_create_view(request):
    """
    View function for creating a new crystal data entry.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        If the request method is GET, returns a rendered HTML template containing a form for creating a new crystal data entry.
        If the request method is POST and the form is valid, saves the form data to the database and redirects to the database list view.
        If the request method is POST and the form is invalid, returns a rendered HTML template containing the invalid form.
    """

    form = CrystalDataForm(request.FILES)
    if request.method == "POST":
        form = CrystalDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("d_spacing:database_list"))

    context = {"form": form}
    return render(request, "d_spacing/crystal_data_create.html", context)


class UpdateCrystalDataView(LoginRequiredMixin, UpdateView):
    """
    View for updating CrystalData model instance.

    Attributes:
    - model: CrystalData model
    - form_class: CrystalDataForm
    - template_name: HTML template for rendering the view
    - success_url: URL to redirect to after successful form submission
    """

    model = CrystalData
    form_class = CrystalDataForm
    template_name = "d_spacing/update_crystal_data.html"
    success_url = reverse_lazy("d_spacing:database_list")

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the view.

        Returns:
        - If user is authorized to update the material data, returns the view with the form.
        - If user is not authorized, returns a warning message and redirects to the database list view.
        """
        crystal_data = self.get_object()
        if crystal_data.uploaded_by != request.user:
            messages.warning(
                request, "You are not authorized to update this material data."
            )
            return redirect(reverse("d_spacing:database_list"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for the view.

        Returns:
        - If user is authorized to update the material data, saves the form and returns a success message.
        - If user is not authorized, returns a warning message and redirects to the database list view.
        """
        crystal_data = self.get_object()
        if crystal_data.uploaded_by != request.user:
            messages.warning(
                request, "You are not authorized to update this material data."
            )
            return redirect(reverse("d_spacing:database_list"))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Handles valid form submissions.

        Returns:
        - Returns a success message and calls the parent form_valid method.
        """
        messages.success(self.request, "Material data successfully updated.")
        return super().form_valid(form)


# class DeleteCrystalDataView(LoginRequiredMixin, ListView):
#     """
#     A view that allows a user to delete one or more CrystalData objects.

#     Inherits from Django's built-in ListView class and adds authorization checks
#     to ensure that only the user who uploaded the CrystalData objects can delete them.

#     Attributes:
#     - model (CrystalData): The model that this view operates on.
#     - template_name (str): The name of the template to use for rendering the view.

#     Methods:
#     - get_queryset(self): Returns the queryset of CrystalData objects to display.
#     - post(self, request, *args, **kwargs): Handles POST requests to the view.
#     """

#     model = CrystalData
#     template_name = "d_spacing/delete_crystal_data.html"

#     def get_queryset(self):
#         """
#         Returns the queryset of CrystalData objects to display.

#         Filters the queryset to only include objects uploaded by the authenticated user.

#         Returns:
#         - QuerySet: The queryset of CrystalData objects to display.
#         """
#         return CrystalData.objects.filter(uploaded_by=self.request.user)

#     def post(self, request):
#         """
#         Handles POST requests to the view.

#         Deletes the selected CrystalData objects and redirects to the success URL.

#         Returns:
#         - redirect(self.success_url): A redirect to the success URL.
#         """
#         selected_ids = request.POST.getlist("selected_ids")
#         selected_objects = CrystalData.objects.filter(
#             id__in=selected_ids, uploaded_by=request.user
#         )
#         if request.POST.get("confirm_delete"):
#             selected_objects.delete()
#             return redirect(reverse_lazy("d_spacing:user_database_list"))


class DeleteCrystalDataView(LoginRequiredMixin, DeleteView):
    """
    A view that allows a user to delete a CrystalData object.

    Inherits from Django's built-in DeleteView class and adds authorization checks
    to ensure that only the user who uploaded the CrystalData object can delete it.

    Attributes:
    - model (CrystalData): The model that this view operates on.
    - template_name (str): The name of the template to use for rendering the view.
    - success_url (str): The URL to redirect to after a successful deletion.

    Methods:
    - get(self, request, *args, **kwargs): Handles GET requests to the view.
    - post(self, request, *args, **kwargs): Handles POST requests to the view.
    """

    model = CrystalData
    template_name = "d_spacing/delete_crystal_data.html"
    success_url = reverse_lazy("d_spacing:database_list")

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to the view.

        Checks if the user is authorized to delete the CrystalData object, and if not,
        redirects them to the database list page with a warning message.

        Returns:
        - super().get(request, *args, **kwargs): The parent class's get method.
        """
        crystal_data = self.get_object()
        if crystal_data.uploaded_by != request.user:
            messages.warning(
                request, "You are not authorized to delete this material data."
            )
            return redirect(reverse("d_spacing:database_list"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to the view.

        Checks if the user is authorized to delete the CrystalData object, and if not,
        redirects them to the database list page with a warning message. If the deletion
        is successful, displays a success message.

        Returns:
        - super().post(request, *args, **kwargs): The parent class's post method.
        """
        crystal_data = self.get_object()
        if crystal_data.uploaded_by != request.user:
            messages.warning(
                request, "You are not authorized to delete this material data."
            )
            return redirect(reverse("d_spacing:database_list"))
        messages.success(request, "Material data successfully deleted.")
        return super().post(request, *args, **kwargs)


def dspacing_results_view(request, crystal_id):
    try:
        info = get_object_or_404(CrystalData, id=crystal_id)

    except CrystalData.DoesNotExist:
        return HttpResponse("crystal not found", status=404)

    try:
        unit_cell_length_a = float(info.cell_length_a)
        unit_cell_length_b = float(info.cell_length_b)
        unit_cell_length_c = float(info.cell_length_c)
        unit_cell_angle_alpha = float(info.cell_angle_alpha)
        unit_cell_angle_beta = float(info.cell_angle_beta)
        unit_cell_angle_gamma = float(info.cell_angle_gamma)

    except ValueError:
        return HttpResponse("Invalid input data", staus=400)

    crystal_system = info.crystal_system
    space_group_it_number = info.space_group_it_number

    analyzer = CrystalAnalyzer(
        unit_cell_length_a,
        unit_cell_length_b,
        unit_cell_length_c,
        unit_cell_angle_alpha,
        unit_cell_angle_beta,
        unit_cell_angle_gamma,
        crystal_system,
        space_group_it_number,
    )

    miller_index_results = []

    for miller_index_h in range(1, 3):
        for miller_index_k in range(0, 4):
            for miller_index_l in range(0, 4):
                d_spacing = analyzer.calculate_d_spacing(
                    miller_index_h,
                    miller_index_k,
                    miller_index_l,
                ).__round__(4)
                if d_spacing is not None:
                    miller_index_results.append(
                        (
                            miller_index_h,
                            miller_index_k,
                            miller_index_l,
                            d_spacing,
                        )
                    )

    miller_index_results.sort(key=lambda x: x[3], reverse=True)
    # print(list_of_results)

    print(f"The determined crystal structure is: {analyzer.crystal_system}")
    print("Miller Index (hkl) - D-spacing results:")
    for result in miller_index_results:
        print(f"({result[0]}, {result[1]}, {result[2]}) - {result[3]:.4f} Å")

    context = {
        "crystal_id": crystal_id,
        "crystal_name": info.crystal_name,
        "crystal_formula": info.crystal_formula,
        "crystal_system": info.crystal_system,
        "cell_length_a": info.cell_length_a,
        "cell_length_b": info.cell_length_b,
        "cell_length_c": info.cell_length_c,
        "cell_angle_alpha": info.cell_angle_alpha,
        "cell_angle_beta": info.cell_angle_beta,
        "cell_angle_gamma": info.cell_angle_gamma,
        "space_group_it_number": info.space_group_it_number,
        "symmetry_space_group_name_H_M": info.symmetry_space_group_name_H_M,
        "list_of_results": miller_index_results,
    }

    return render(request, "d_spacing/dspacing_results.html", context)

    # @login_required
    # def upload_cif_file_view(request):
    if request.method == "POST":
        form = CifCrystalDataForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist("cif_file")
        if form.is_valid():
            total_files = len(files)
            for i, file in enumerate(files):
                file_instance = CrystalData.objects.create(
                    cif_file=file, uploaded_by=request.user
                )
                file_instance.save()

                progress = (i + 1) / total_files * 100

                file_path = file_instance.cif_file.path
                instance_id = file_instance.id

                xtl = dif.Crystal(file_path)
                doc = cif.read_file(file_path)
                block = doc.sole_block()

                CrystalData.objects.filter(id=instance_id).update(
                    crystal_name=str(
                        block.find_value("_chemical_name_mineral")
                        or block.find_value("_chemical_name_systematic")
                    ),
                    crystal_formula=str(block.find_value("_chemical_formula_sum")),
                    cell_length_a=float(xtl.Cell.a),
                    cell_length_b=float(xtl.Cell.b),
                    cell_length_c=float(xtl.Cell.c),
                    cell_angle_alpha=float(xtl.Cell.alpha),
                    cell_angle_beta=float(xtl.Cell.beta),
                    cell_angle_gamma=float(xtl.Cell.gamma),
                    space_group_it_number=block.find_value("_space_group_IT_number")
                    or block.find_value("_symmetry_Int_Tables_number"),
                    symmetry_space_group_name_H_M=block.find_value(
                        "_symmetry_space_group_name_H-M"
                    ),
                    crystal_system=str(
                        block.find_value("_symmetry_cell_setting")
                        or block.find_value("_space_group_crystal_system")
                    ),
                )

            messages.success(request, "CIF file(s) uploaded successfully!")
            return redirect(reverse("d_spacing:database_list"))
    else:
        form = CifCrystalDataForm()

    return render(request, "d_spacing/upload_cif_file.html", {"form": form})


class UploadCifFileView(LoginRequiredMixin, View):
    form_class = CifCrystalDataForm
    template_name = "d_spacing/upload_cif_file.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES or None)
        files = request.FILES.getlist("cif_file")
        if form.is_valid():
            total_files = len(files)
            for i, file in enumerate(files):
                file_instance = CrystalData.objects.create(
                    cif_file=file, uploaded_by=request.user
                )
                file_instance.save()
                # first_name = get_first_name_from_email(request.user.email)

                progress = (i + 1) / total_files * 100

                file_path = file_instance.cif_file.path
                instance_id = file_instance.id

                parse_cif_file(file_path, instance_id)

            messages.success(request, "CIF file(s) uploaded successfully!")
            return redirect(reverse("d_spacing:database_list"))
        else:
            messages.error(request, "Invalid form submission.")
            context = {"form": form, "first_name": first_name}
            return render(request, self.template_name, context)


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
        "crystal_id": crystal_id,
        "crystal_name": info.crystal_name,
        "crystal_formula": info.crystal_formula,
        "crystal_system": info.crystal_system,
        "cell_length_a": info.cell_length_a,
        "cell_length_b": info.cell_length_b,
        "cell_length_c": info.cell_length_c,
        "cell_angle_alpha": info.cell_angle_alpha,
        "cell_angle_beta": info.cell_angle_beta,
        "cell_angle_gamma": info.cell_angle_gamma,
        "space_group_it_number": info.space_group_IT_number,
        "symmetry_space_group_name_H_M": info.symmetry_space_group_name_H_M,
        "cif_file": info.cif_file,
        # 'cif_info' : cif_info,
    }

    return render(request, "d_spacing/cif_file_display.html", context)
