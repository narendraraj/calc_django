import math



def determine_crystal_structure_1(space_group_it_number):
    if space_group_it_number in range(0, 3):
        return "triclinic"
    elif space_group_it_number in range(3,16):
        return "monoclinic"
    elif space_group_it_number in  range(15,75):
        return "orthorhombic"
    elif space_group_it_number in  range(74,143):
        return "tetragonal"
    elif space_group_it_number in  range(142,168):
        return "rhombohedral"
    elif  space_group_it_number in  range(167,195):
        return "hexagonal"
    elif space_group_it_number in range(194,231):
        return "cubic"
    else:
        return "None"






class CrystalAnalyzer:
    def __init__(self, unit_cell_length_a, unit_cell_length_b, unit_cell_length_c, unit_cell_angle_alpha, unit_cell_angle_beta, unit_cell_angle_gamma):
        self.unit_cell_length_a = unit_cell_length_a
        self.unit_cell_length_b = unit_cell_length_b
        self.unit_cell_length_c = unit_cell_length_c
        self.unit_cell_angle_alpha = unit_cell_angle_alpha
        self.unit_cell_angle_beta = unit_cell_angle_beta
        self.unit_cell_angle_gamma = unit_cell_angle_gamma
        # self.miller_index_h = miller_index_h
        # self.miller_index_k = miller_index_k
        # self.miller_index_l = miller_index_l
        # self.structure_1 = self.determine_crystal_structure_1()
        self.structure = self.determine_crystal_structure_2()




    def determine_crystal_structure_2(self):
        if self.unit_cell_length_a == self.unit_cell_length_b == self.unit_cell_length_c and self.unit_cell_angle_alpha == 90 and self.unit_cell_angle_beta == 90 and self.unit_cell_angle_gamma == 90.0:
            return "cubic"
        elif self.unit_cell_length_a == self.unit_cell_length_b != self.unit_cell_length_c and self.unit_cell_angle_alpha == 90 and self.unit_cell_angle_beta == 90 and self.unit_cell_angle_gamma == 90.0:
            return "tetragonal"
        elif self.unit_cell_length_a != self.unit_cell_length_b != self.unit_cell_length_c and self.unit_cell_angle_alpha == 90 and self.unit_cell_angle_beta == 90 and self.unit_cell_angle_gamma == 90.0:
            return "orthorhombic"
        elif self.unit_cell_length_a == self.unit_cell_length_b == self.unit_cell_length_c and self.unit_cell_angle_alpha != 90.0 and self.unit_cell_angle_beta != 90.0 and self.unit_cell_angle_gamma != 90.0 and self.unit_cell_angle_alpha == self.unit_cell_angle_beta == self.unit_cell_angle_gamma:
            return "rhombohedral"
        elif self.unit_cell_length_a == self.unit_cell_length_b != self.unit_cell_length_c and self.unit_cell_angle_alpha == 90 and self.unit_cell_angle_beta == 90 and self.unit_cell_angle_gamma == 120.0:
            return "hexagonal"
        elif self.unit_cell_length_a != self.unit_cell_length_b != self.unit_cell_length_c and self.unit_cell_angle_alpha == 90 and self.unit_cell_angle_beta == 90 and self.unit_cell_angle_gamma != 90.0:
            return "monoclinic"
        elif self.unit_cell_length_a != self.unit_cell_length_b != self.unit_cell_length_c and self.unit_cell_angle_alpha != 90 and self.unit_cell_angle_beta != 90 and self.unit_cell_angle_gamma != 90.0:
            return "triclinic"
        else:
            return "Unknown"

    def calculate_d_spacing_cubic(self):
        d_spacing = self.unit_cell_length_a / math.sqrt(self.miller_index_h ** 2 + self.miller_index_k ** 2 + self.miller_index_l ** 2)
        return d_spacing

    def calculate_d_spacing_tetragonal(self):
        d_spacing = self.unit_cell_length_c / math.sqrt(self.miller_index_h ** 2 + self.miller_index_k ** 2 + (self.miller_index_l ** 2 / (self.unit_cell_length_c ** 2 / self.unit_cell_length_a ** 2)))
        return d_spacing

    def calculate_d_spacing_orthorhombic(self):
        d_spacing = math.sqrt((self.miller_index_h ** 2 / self.unit_cell_length_a ** 2) + (self.miller_index_k ** 2 / self.unit_cell_length_b ** 2) + (self.miller_index_l ** 2 / self.unit_cell_length_c ** 2)) ** (-1)
        return d_spacing

    def calculate_d_spacing_hexagonal(self):
        d_spacing = self.unit_cell_length_c / math.sqrt(4 * (self.miller_index_h ** 2 + self.miller_index_h * self.miller_index_k + self.miller_index_k ** 2) / 3 + self.miller_index_l ** 2)
        return d_spacing

    def calculate_d_spacing_monoclinic(self):
        beta_rad = math.radians(self.unit_cell_angle_beta)
        d_spacing = math.sqrt(
            (self.miller_index_h ** 2 / self.unit_cell_length_a ** 2) + (self.miller_index_k ** 2 / self.unit_cell_length_b ** 2) + (self.miller_index_l ** 2 / self.unit_cell_length_c ** 2 - 2 * self.miller_index_h * self.miller_index_l * math.cos(beta_rad) / (self.unit_cell_length_a * self.unit_cell_length_c))) ** (-1)
        return d_spacing

    def calculate_d_spacing_triclinic(self):
        alpha_rad = math.radians(self.unit_cell_angle_alpha)
        beta_rad = math.radians(self.unit_cell_angle_beta)
        gamma_rad = math.radians(self.unit_cell_angle_gamma)

        # V = self.unit_cell_length_a * self.unit_cell_length_b * self.unit_cell_length_c * math.sqrt(
        #     1 - math.cos(alpha_rad) ** 2 - math.cos(beta_rad) ** 2 - math.cos(gamma_rad) ** 2 + 2 * math.cos(
        #         alpha_rad) * math.cos(beta_rad) * math.cos(gamma_rad))
        # d_spacing = V / math.sqrt(self.miller_index_h ** 2 / self.unit_cell_length_a ** 2 + self.miller_index_k ** 2 / self.unit_cell_length_b ** 2 + self.miller_index_l ** 2 / self.unit_cell_length_c ** 2)
        # return d_spacing
        d_spacing = 1 / math.sqrt(
            (self.miller_index_h ** 2 / self.unit_cell_length_a ** 2) + (self.miller_index_k ** 2 / self.unit_cell_length_b ** 2) + (
                        self.miller_index_l ** 2 / self.unit_cell_length_c ** 2) - 2 * (
                        self.miller_index_h * self.miller_index_k * math.cos(alpha_rad) / (
                            self.unit_cell_length_a * self.unit_cell_length_b)) - 2 * (
                        self.miller_index_k * self.miller_index_l * math.cos(beta_rad) / (
                            self.unit_cell_length_b * self.unit_cell_length_c)) - 2 * (
                        self.miller_index_h * self.miller_index_l * math.cos(gamma_rad) / (
                            self.unit_cell_length_a * self.unit_cell_length_c)))
        return d_spacing

    def calculate_d_spacing_rhombohedral(self):
        alpha_rad = math.radians(self.unit_cell_angle_alpha)
        d_spacing = self.unit_cell_length_a / math.sqrt((self.miller_index_h ** 2 + self.miller_index_k ** 2 + self.miller_index_l ** 2) + 2 * self.miller_index_h * self.miller_index_k * (1 - math.cos(alpha_rad)))
        return d_spacing

    def calculate_d_spacing(self,  miller_index_h, miller_index_k, miller_index_l):
        self.miller_index_h = miller_index_h
        self.miller_index_k = miller_index_k
        self.miller_index_l = miller_index_l
        if self.structure == "cubic":
            return self.calculate_d_spacing_cubic()
        elif self.structure == "tetragonal":
            return self.calculate_d_spacing_tetragonal()
        elif self.structure == "hexagonal":
            return self.calculate_d_spacing_hexagonal()
        elif self.structure == "orthorhombic":
            return self.calculate_d_spacing_orthorhombic()
        elif self.structure == "monoclinic":
            return self.calculate_d_spacing_monoclinic()
        elif self.structure == "triclinic":
            return self.calculate_d_spacing_triclinic()
        elif self.structure == "rhombohedral":
            return self.calculate_d_spacing_rhombohedral()
        else:
            return "Not applicable"






