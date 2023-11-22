import os


from django.http import HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .models import CrystalData

from .forms import CrystalDataForm, CifCrystalDataForm
from .utils import parse_cif_file

import mimetypes

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
    # response1 = requests.post(
    #     url,
    #     headers={'Content-Type': 'application/json'},
    #     data=request_body
    # )
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
    # response2 = requests.post(
    #     url,
    #     headers={'Content-Type': 'application/json'},
    #     data=request_body
    # )
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
    """A view that displays a list of CrystalData objects.

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
        """Returns the queryset of CrystalData objects to display.

        If a search query is provided in the request, filters the queryset to include
        only objects that match the query.

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
    """A view that displays a list of CrystalData objects uploaded by the current user.

    Attributes:
        model (CrystalData): The model that this view displays.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the context variable to use in the
        template.
        paginate_by (int): The number of objects to display per page.

    Methods:
        get_queryset(): Returns the queryset of CrystalData objects to display.
    """

    model = CrystalData
    template_name = "d_spacing/user_database_list.html"
    context_object_name = "object_list"
    paginate_by = 20

    def get_queryset(self):
        """Returns the queryset of CrystalData objects to display.

        If a search query is provided in the request, filters the queryset to include
        only objects that match the query and were uploaded by the current user.
        Otherwise, returns all objects uploaded by the current user.
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
    """A custom paginator class that extends Django's built-in Paginator class.

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
    """View function for creating a new crystal data entry.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        If the request method is GET, returns a rendered HTML template containing a
        form for creating a new crystal data entry.
        If the request method is POST and the form is valid, saves the form data to the
        database and redirects to the database list view.
        If the request method is POST and the form is invalid, returns a rendered HTML
        template containing the invalid form.
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
    """View for updating CrystalData model instance.

    Attributes:
    - model: CrystalData model
    - form_class: CrystalDataForm
    - template_name: HTML template for rendering the view
    - success_url: URL to redirect to after successful form submission
    """

    model = CrystalData
    form_class = CrystalDataForm
    template_name = "d_spacing/update_crystal_data.html"
    success_url = reverse_lazy("d_spacing:user_database_list")

    def get(self, request, *args, **kwargs):
        """Handles GET requests for the view.

        Returns:
        - If user is authorized to update the material data, returns the view with the
        form.
        - If user is not authorized, returns a warning message and redirects to the
        database list view.
        """
        crystal_data = self.get_object()
        if crystal_data.uploaded_by != request.user:
            messages.warning(
                request, "You are not authorized to update this material data."
            )
            return redirect(reverse("d_spacing:database_list"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handles POST requests for the view.

        Returns:
        - If user is authorized to update the material data, saves the form and returns
        a success message.
        - If user is not authorized, returns a warning message and redirects to the
        database list view.
        """
        crystal_data = self.get_object()
        if crystal_data.uploaded_by != request.user:
            messages.warning(
                request, "You are not authorized to update this material data."
            )
            return redirect(reverse("d_spacing:database_list"))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """Handles valid form submissions.

        Returns:
        - Returns a success message and calls the parent form_valid method.
        """
        messages.success(self.request, "Material data successfully updated.")
        return super().form_valid(form)


class DeleteCrystalDataView(LoginRequiredMixin, DeleteView):
    """A view that allows a user to delete a CrystalData object.

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
    success_url = reverse_lazy("d_spacing:user_database_list")

    def get(self, request, *args, **kwargs):
        """Handles GET requests to the view.

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
        """Handles POST requests to the view.

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


class DSpacingResultsView(View):
    """
    View class for displaying D-spacing results.

    This view calculates the D-spacing values for a given crystal and renders
    them in a template along with other relevant information about the crystal.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = "d_spacing/dspacing_results.html"

    def get(self, request, crystal_id):
        try:
            object = get_object_or_404(CrystalData, id=crystal_id)
        except CrystalData.DoesNotExist:
            return HttpResponse("crystal not found", status=404)

        try:
            unit_cell_length_a = float(object.cell_length_a)
            unit_cell_length_b = float(object.cell_length_b)
            unit_cell_length_c = float(object.cell_length_c)
            unit_cell_angle_alpha = float(object.cell_angle_alpha)
            unit_cell_angle_beta = float(object.cell_angle_beta)
            unit_cell_angle_gamma = float(object.cell_angle_gamma)
        except ValueError:
            return HttpResponse("Invalid input data", status=400)

        crystal_system = object.crystal_system
        space_group_it_number = object.space_group_it_number

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

        miller_index_results = [
            (
                miller_index_h,
                miller_index_k,
                miller_index_l,
                analyzer.calculate_d_spacing(
                    miller_index_h, miller_index_k, miller_index_l
                ).__round__(4),
            )
            for miller_index_h in range(1, 3)
            for miller_index_k in range(4)
            for miller_index_l in range(4)
            if analyzer.calculate_d_spacing(
                miller_index_h, miller_index_k, miller_index_l
            )
            is not None
        ]
        miller_index_results.sort(key=lambda x: x[3], reverse=True)

        context = {
            "crystal_id": crystal_id,
            "crystal_name": object.crystal_name,
            "crystal_formula": object.crystal_formula,
            "crystal_system": object.crystal_system,
            "cell_length_a": object.cell_length_a,
            "cell_length_b": object.cell_length_b,
            "cell_length_c": object.cell_length_c,
            "cell_angle_alpha": object.cell_angle_alpha,
            "cell_angle_beta": object.cell_angle_beta,
            "cell_angle_gamma": object.cell_angle_gamma,
            "space_group_it_number": object.space_group_it_number,
            "symmetry_space_group_name_H_M": object.symmetry_space_group_name_H_M,
            "list_of_results": miller_index_results,
        }

        return render(request, self.template_name, context)


class UploadCifFileView(LoginRequiredMixin, View):
    """
    View for uploading CIF files and saving them to the database.

    Inherits from LoginRequiredMixin and View.
    """

    form_class = CifCrystalDataForm
    template_name = "d_spacing/upload_cif_file.html"

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the upload CIF file view.

        Creates an instance of the form and renders the template with the form.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - The rendered template with the form.
        """
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for the upload CIF file view.

        Validates the form and saves the uploaded CIF files to the database.
        If the form is valid, each file is saved as a CrystalData object and
        then parsed using the parse_cif_file function. Success or error messages
        are displayed to the user.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the form is valid, redirects to the user database list view.
        - If the form is invalid, renders the template with the form and error message.
        """
        form = self.form_class(request.POST or None, request.FILES or None)
        files = request.FILES.getlist("cif_file")
        if form.is_valid():
            # total_files = len(files)
            for i, file in enumerate(files):
                file_instance = CrystalData.objects.create(
                    cif_file=file, uploaded_by=request.user
                )
                file_instance.save()

                # progress = (i + 1) / total_files * 100

                file_path = file_instance.cif_file.path
                instance_id = file_instance.id

                parse_cif_file(file_path, instance_id)

            messages.success(request, "CIF file(s) uploaded successfully!")
            return redirect(reverse("d_spacing:user_database_list"))
        else:
            messages.error(request, "Invalid form submission.")
            context = {"form": form}
            return render(request, self.template_name, context)


def cif_file_display_view(request, crystal_id):
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
        "space_group_it_number": info.space_group_it_number,
        "symmetry_space_group_name_H_M": info.symmetry_space_group_name_H_M,
        # "cif_file": info.cif_file,
        # "cif_info": cif_info,
    }

    return render(request, "d_spacing/cif_file_display.html", context)


def download_cif_file(request, id):
    cif_file = get_object_or_404(CrystalData, id=id)
    file_path = cif_file.cif_file.path

    content_type, encoding = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "text/plain"

    response = FileResponse(open(file_path, "rb"), content_type=content_type)
    response["Content-Length"] = cif_file.cif_file.size
    original_filename = os.path.basename(cif_file.cif_file.name)
    response["Content-Disposition"] = f'attachment; filename="{original_filename}"'

    return response
    # return redirect(reverse("d_spacing:database_list"))
