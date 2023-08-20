#  these the delted functions form d_spaciing view from initial implmnetations. just kept it it if needed later.

def calculate_dspacing(crystal_structure, list_of_abc, list_of_hkl):

    a = float(list_of_abc[0])
    b = float(list_of_abc[1])
    c = float(list_of_abc[2])



    h = list_of_hkl[0]
    k = list_of_hkl[1]
    l = list_of_hkl[2]



    if lower(crystal_structure) == 'cubic':
        d_result = a/(math.sqrt((h ** 2) + (k ** 2) + (l ** 2)))

    if lower(crystal_structure) == 'hexagonal':
        d_result = (math.sqrt((4 / 3) * ((h ** 2) + (h * k) + (k ** 2)
                                         ) / (a ** 2)) + math.sqrt((l ** 2) / (c ** 2))) ** -1
    if lower(crystal_structure) == 'orthorhombic':
        d_result = (math.sqrt((h ** 2 / a ** 2) +
                              (k ** 2 / b ** 2) + (l ** 2 / c ** 2))) ** -1

    if lower(crystal_structure) == 'tetragonal':
        d_result = math.sqrt(
            ((h ** 2 + k ** 2 + l**2*(a/c)**2))*(1 / a ** 2)) ** -1
    return round(d_result, 4)

    # if lower(crystal_structure) == 'monoclinic':
    #     d_result = math.sqrt(1/ sin**2
    #         ((h ** 2 + k ** 2 + l**2*(a/c)**2))*(1 / a ** 2)) ** -1
    # return round(d_result, 4)


# @login_required(redirect_field_name='/')
def dspacing_results_view_test(request, crystal_id):
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
                result = calculate_dspacing(
                    crystal_structure, list_of_abc, [h, k, l])
                # cubic_result = info.cell_length_a/decimal.Decimal((math.sqrt((h ** 2) + (k ** 2) + (l ** 2))))
                # d_results(h,k,l)
                # list_of_results.append([h, k, l, cubic_result])
                list_of_results.append([h, k, l, result])
    list_of_results.sort(key=lambda x: x[3], reverse=True)
    # print(list_of_results)

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

    return render(request, "d_spacing/dspacing_results.html", context)
