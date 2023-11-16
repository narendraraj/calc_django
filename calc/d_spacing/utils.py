from .forms import CifCrystalDataForm
from .models import CrystalData
import Dans_Diffraction as dif
from gemmi import cif


def parse_cif_file(file_path, instance_id):
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
