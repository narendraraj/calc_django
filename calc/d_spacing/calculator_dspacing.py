import math


class CrystalAnalyzer:
    def __init__(
        self,
        unit_cell_length_a,
        unit_cell_length_b,
        unit_cell_length_c,
        unit_cell_angle_alpha,
        unit_cell_angle_beta,
        unit_cell_angle_gamma,
        crystal_system=None,
        space_group_it_number=None,
    ):
        self.unit_cell_length_a = unit_cell_length_a
        self.unit_cell_length_b = unit_cell_length_b
        self.unit_cell_length_c = unit_cell_length_c
        self.unit_cell_angle_alpha = unit_cell_angle_alpha
        self.unit_cell_angle_beta = unit_cell_angle_beta
        self.unit_cell_angle_gamma = unit_cell_angle_gamma

        print(f"{type(crystal_system)=}")
        print(f"{type(space_group_it_number)=}")

        if crystal_system != "None":
            self.crystal_system = crystal_system

        elif crystal_system == "None" and type(space_group_it_number) is int:
            self.crystal_system = self.determine_crystal_structure_1(
                space_group_it_number
            )

        else:
            self.crystal_system = self.determine_crystal_structure_2()

    # Define the method to determine crystal structure using space_group_it_number
    def determine_crystal_structure_1(self, space_group_it_number):
        if space_group_it_number in range(0, 3):
            return "triclinic"
        elif space_group_it_number in range(3, 16):
            return "monoclinic"
        elif space_group_it_number in range(15, 75):
            return "orthorhombic"
        elif space_group_it_number in range(74, 143):
            return "tetragonal"
        elif space_group_it_number in range(142, 168):
            return "rhombohedral"
        elif space_group_it_number in range(167, 195):
            return "hexagonal"
        elif space_group_it_number in range(194, 231):
            return "cubic"
        else:
            return "Nothing"

    def determine_crystal_structure_2(self):
        if (
            self.unit_cell_length_a
            == self.unit_cell_length_b
            == self.unit_cell_length_c
            and self.unit_cell_angle_alpha == 90
            and self.unit_cell_angle_beta == 90
            and self.unit_cell_angle_gamma == 90.0
        ):
            return "cubic"
        elif (
            self.unit_cell_length_a
            == self.unit_cell_length_b
            != self.unit_cell_length_c
            and self.unit_cell_angle_alpha == 90
            and self.unit_cell_angle_beta == 90
            and self.unit_cell_angle_gamma == 90.0
        ):
            return "tetragonal"
        elif (
            self.unit_cell_length_a
            != self.unit_cell_length_b
            != self.unit_cell_length_c
            and self.unit_cell_angle_alpha == 90
            and self.unit_cell_angle_beta == 90
            and self.unit_cell_angle_gamma == 90.0
        ):
            return "orthorhombic"
        elif (
            self.unit_cell_length_a
            == self.unit_cell_length_b
            == self.unit_cell_length_c
            and self.unit_cell_angle_alpha != 90.0
            and self.unit_cell_angle_beta != 90.0
            and self.unit_cell_angle_gamma != 90.0
            and self.unit_cell_angle_alpha
            == self.unit_cell_angle_beta
            == self.unit_cell_angle_gamma
        ):
            return "rhombohedral"
        elif (
            self.unit_cell_length_a
            == self.unit_cell_length_b
            != self.unit_cell_length_c
            and self.unit_cell_angle_alpha == 90
            and self.unit_cell_angle_beta == 90
            and self.unit_cell_angle_gamma == 120.0
        ):
            return "hexagonal"
        elif (
            self.unit_cell_length_a
            != self.unit_cell_length_b
            != self.unit_cell_length_c
            and self.unit_cell_angle_alpha == 90
            and self.unit_cell_angle_beta == 90
            and self.unit_cell_angle_gamma != 90.0
        ):
            return "monoclinic"
        elif (
            self.unit_cell_length_a
            != self.unit_cell_length_b
            != self.unit_cell_length_c
            and self.unit_cell_angle_alpha != 90
            and self.unit_cell_angle_beta != 90
            and self.unit_cell_angle_gamma != 90.0
        ):
            return "triclinic"
        else:
            return None

    # Methods for calculating d-spacing for different crystal systems
    def calculate_d_spacing_cubic(self, miller_index_h, miller_index_k, miller_index_l):
        d_spacing = self.unit_cell_length_a / math.sqrt(
            miller_index_h**2 + miller_index_k**2 + miller_index_l**2
        )
        return d_spacing

    def calculate_d_spacing_tetragonal(
        self, miller_index_h, miller_index_k, miller_index_l
    ):
        d_spacing = self.unit_cell_length_c / math.sqrt(
            miller_index_h**2
            + miller_index_k**2
            + (
                miller_index_l**2
                / (self.unit_cell_length_c**2 / self.unit_cell_length_a**2)
            )
        )
        return d_spacing

    def calculate_d_spacing_orthorhombic(
        self, miller_index_h, miller_index_k, miller_index_l
    ):
        d_spacing = math.sqrt(
            (miller_index_h**2 / self.unit_cell_length_a**2)
            + (miller_index_k**2 / self.unit_cell_length_b**2)
            + (miller_index_l**2 / self.unit_cell_length_c**2)
        ) ** (-1)
        return d_spacing

    def calculate_d_spacing_hexagonal(
        self, miller_index_h, miller_index_k, miller_index_l
    ):
        d_spacing = self.unit_cell_length_c / math.sqrt(
            4
            * (
                miller_index_h**2
                + miller_index_h * miller_index_k
                + miller_index_k**2
            )
            / 3
            + miller_index_l**2
        )
        return d_spacing

    def calculate_d_spacing_monoclinic(
        self, miller_index_h, miller_index_k, miller_index_l
    ):
        beta_rad = math.radians(self.unit_cell_angle_beta)
        d_spacing = math.sqrt(
            (miller_index_h**2 / self.unit_cell_length_a**2)
            + (miller_index_k**2 / self.unit_cell_length_b**2)
            + (
                miller_index_l**2 / self.unit_cell_length_c**2
                - 2
                * miller_index_h
                * miller_index_l
                * math.cos(beta_rad)
                / (self.unit_cell_length_a * self.unit_cell_length_c)
            )
        ) ** (-1)
        return d_spacing

    def calculate_d_spacing_triclinic(
        self, miller_index_h, miller_index_k, miller_index_l
    ):
        alpha_rad = math.radians(self.unit_cell_angle_alpha)
        beta_rad = math.radians(self.unit_cell_angle_beta)
        gamma_rad = math.radians(self.unit_cell_angle_gamma)

        d_spacing = 1 / math.sqrt(
            (miller_index_h**2 / self.unit_cell_length_a**2)
            + (miller_index_k**2 / self.unit_cell_length_b**2)
            + (miller_index_l**2 / self.unit_cell_length_c**2)
            - 2
            * (
                miller_index_h
                * miller_index_k
                * math.cos(alpha_rad)
                / (self.unit_cell_length_a * self.unit_cell_length_b)
            )
            - 2
            * (
                miller_index_k
                * miller_index_l
                * math.cos(beta_rad)
                / (self.unit_cell_length_b * self.unit_cell_length_c)
            )
            - 2
            * (
                miller_index_h
                * miller_index_l
                * math.cos(gamma_rad)
                / (self.unit_cell_length_a * self.unit_cell_length_c)
            )
        )
        return d_spacing

    def calculate_d_spacing_rhombohedral(
        self, miller_index_h, miller_index_k, miller_index_l
    ):
        alpha_rad = math.radians(self.unit_cell_angle_alpha)
        d_spacing = self.unit_cell_length_a / math.sqrt(
            (miller_index_h**2 + miller_index_k**2 + miller_index_l**2)
            + 2 * miller_index_h * miller_index_k * (1 - math.cos(alpha_rad))
        )
        return d_spacing

    def calculate_d_spacing(self, miller_index_h, miller_index_k, miller_index_l):
        # Calculate d-spacing based on the crystal system
        if self.crystal_system == "cubic":
            return self.calculate_d_spacing_cubic(
                miller_index_h, miller_index_k, miller_index_l
            )
        elif self.crystal_system == "tetragonal":
            return self.calculate_d_spacing_tetragonal(
                miller_index_h, miller_index_k, miller_index_l
            )
        elif self.crystal_system == "hexagonal":
            return self.calculate_d_spacing_hexagonal(
                miller_index_h, miller_index_k, miller_index_l
            )
        elif self.crystal_system == "orthorhombic":
            return self.calculate_d_spacing_orthorhombic(
                miller_index_h, miller_index_k, miller_index_l
            )
        elif self.crystal_system == "monoclinic":
            return self.calculate_d_spacing_monoclinic(
                miller_index_h, miller_index_k, miller_index_l
            )
        elif self.crystal_system == "triclinic":
            return self.calculate_d_spacing_triclinic(
                miller_index_h, miller_index_k, miller_index_l
            )
        elif self.crystal_system == "rhombohedral":
            return self.calculate_d_spacing_rhombohedral(
                miller_index_h, miller_index_k, miller_index_l
            )
        else:
            return 00.000

    # def calculate_d_spacing(self, miller_index_h, miller_index_k, miller_index_l, crystal_system):
    #     # Calculate d-spacing based on the crystal system
    #     if crystal_system == "cubic":
    #         return self.calculate_d_spacing_cubic(
    #             miller_index_h, miller_index_k, miller_index_l
    #         )
    #     elif crystal_system == "tetragonal":
    #         return self.calculate_d_spacing_tetragonal(
    #             miller_index_h, miller_index_k, miller_index_l
    #         )
    #     elif crystal_system == "hexagonal":
    #         return self.calculate_d_spacing_hexagonal(
    #             miller_index_h, miller_index_k, miller_index_l
    #         )
    #     elif crystal_system == "orthorhombic":
    #         return self.calculate_d_spacing_orthorhombic(
    #             miller_index_h, miller_index_k, miller_index_l
    #         )
    #     elif crystal_system == "monoclinic":
    #         return self.calculate_d_spacing_monoclinic(
    #             miller_index_h, miller_index_k, miller_index_l
    #         )
    #     elif crystal_system == "triclinic":
    #         return self.calculate_d_spacing_triclinic(
    #             miller_index_h, miller_index_k, miller_index_l
    #         )
    #     elif crystal_system == "rhombohedral":
    #         return self.calculate_d_spacing_rhombohedral(
    #             miller_index_h, miller_index_k, miller_index_l
    #         )
    #     else:
    #         return None
