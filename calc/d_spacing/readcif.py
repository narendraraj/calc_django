import sys
import os
import re
import json
# import numpy as np
from warnings import warn


def readcif(filename=None, debug=False):
    """
    Open a Crystallographic Information File (*.cif) file and store all entries in a key:value dictionary
     Looped values are stored as lists under a single key entry
     All values are stored as strings
    E.G.
      crys=readcif('somefile.cif')
      crys['_cell_length_a'] = '2.835(2)'
    crys[key] = value
    available keys are give by crys.keys()
    To debug the file with outputted messages, use:
      cif = readcif(file, debug=True)
    Some useful standard CIF keywords:
        _cell_length_a
        _cell_length_b
        _cell_length_c
        _cell_angle_alpha
        _cell_angle_beta
        _cell_angle_gamma
        _space_group_symop_operation_xyz
        _atom_site_label
        _atom_site_type_symbol
        _atom_site_occupancy
        _atom_site_U_iso_or_equiv
        _atom_site_fract_x
        _atom_site_fract_y
        _atom_site_fract_z
    """

    # Get file name
    filename = os.path.abspath(os.path.expanduser(filename))
    (dirName, filetitle) = os.path.split(filename)
    (fname, Ext) = os.path.splitext(filetitle)

    # Open file
    file = open(filename)
    text = file.read()
    file.close()

    # Remove blank lines
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    lines = text.splitlines()

    cifvals = {'Filename': filename, 'Directory': dirName, 'FileTitle': fname}

    # Read file line by line, converting the cif file values to a python dict
    n = 0
    while n < len(lines):
        # Convert line to columns
        vals = lines[n].strip().split()

        # skip empty lines
        if len(vals) == 0:
            n += 1
            continue

        # Search for stored value lines
        if vals[0][0] == '_':
            if len(vals) == 1:
                # Record next lines that are not keys as string
                if lines[n + 1][0] == ';':
                    n += 1
                strarg = []
                while n + 1 < len(lines) and (len(lines[n + 1]) == 0 or lines[n + 1][0].strip() not in ['_', ';']):
                    strarg += [lines[n + 1].strip('\'"')]
                    n += 1
                cifvals[vals[0]] = '\n'.join(strarg)
                chk = 'a'
            else:
                cifvals[vals[0]] = ' '.join(vals[1:]).strip(' \'"\n')
                chk = 'b'
            n += 1
            if debug:
                print('%5d %s %s = %s' % (n, chk, vals[0], cifvals[vals[0]]))
            continue

        # Search for loops
        elif vals[0] == 'loop_':
            n += 1
            loopvals = []
            # Step 1: Assign loop columns
            # looped columns are given by "_column_name"
            while n < len(lines) and len(lines[n].strip()) > 0 and lines[n].strip()[0] == '_':
                loopvals += [lines[n].split()[0]]
                cifvals[loopvals[-1]] = []
                n += 1

            # Step 2: Assign data to columns
            # loops until line has less segments than columns
            while n < len(lines):
                # cols = lines[n].split()
                # this fixes error on symmetry arguments having spaces
                # this will only work if the last argument in the loop is split by spaces (in quotes)
                # cols = cols[:len(loopvals) - 1] + [''.join(cols[len(loopvals) - 1:])]
                cols = [col for col in re.split(
                    "( |\\\".*?\\\"|'.*?')", lines[n]) if col.strip()]
                if len(cols) != len(loopvals):
                    break
                if cols[0][0] == '_' or cols[0] == 'loop_':
                    break  # catches error if loop is only 1 iteration
                if cols[0][0] == '#':
                    n += 1
                    continue  # catches comented out lines
                if len(loopvals) == 1:
                    cifvals[loopvals[0]] += [lines[n].strip(' \"\'\n')]
                else:
                    for c, ll in enumerate(loopvals):
                        cifvals[ll] += [cols[c]]
                n += 1

            if debug:
                for ll in loopvals:
                    print('%5d L %s = %s' % (n, ll, str(cifvals[ll])))
            continue

        else:
            # Skip anything else
            if debug:
                print('%5d SKIPPED: %s' % (n, lines[n]))
            n += 1

    # Replace '.' in keys - fix bug from isodistort cif files
    # e.g. '_space_group_symop_magn_operation.xyz'
    current_keys = list(cifvals.keys())
    for key in current_keys:
        if '.' in key:
            newkey = key.replace('.', '_')
            cifvals[newkey] = cifvals[key]
    return cifvals
    # load_json = json.dumps(cifvals,  indent=4)

    # return json.dumps(cifvals,  indent=4)

    # print(load_json)
    # cif_json =json.loads(load_json)
    # print(cif_json ["_publ_section_title"])

    # print(load_json)

    # with open('json_data.json', 'w') as outfile:
    #     outfile.write(load_json)


# readcif(r"C:\Users\chandran.narendraraj\Desktop\dev\calc_django\calc\media\cif_database\3000000.cif", debug = False)
