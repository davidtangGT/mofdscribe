# -*- coding: utf-8 -*-
"""RASPA force-field builder taken from aiida-lsmo.

MIT License

Copyright 2018-2021, LABORATORY OF MOLECULAR SIMULATION (LSMO),
ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

#ToDo: move this to a standalone-package that can be imported here and in aiida-lsmo
"""
import os
from math import sqrt
from typing import List

import ruamel.yaml as yaml

THISDIR = os.path.dirname(os.path.abspath(__file__))


def check_ff_list(inp_list: List[str]):
    """Check a list of atom types.

    1) Remove duplicates, preserving the order of the elements.
    2) Warn if there are atom types with the same name but different parameters
    3) If a shorter atom type comes later, swap the order # TODO!

    Args:
        inp_list (List[str]): list of atom types

    Raises:
        ValueError: If the list contains duplicate atom type with different parameters

    Returns:
        list[str]: list of atom types
    """ """ """
    out_list = []
    for item in inp_list:
        if item.split()[0] not in [x.split()[0] for x in out_list]:  # atom type label is unique
            out_list.append(item)
        else:
            if item in out_list:  # Two atom types are exactly the same
                pass
            else:
                raise ValueError("Two atom types with same name but different parameters are used.")
    return out_list


def load_yaml():
    """Load the ff_data.yaml as a dict."""
    yamlfullpath = os.path.join(THISDIR, "ff_data.yaml")

    with open(yamlfullpath, "r") as stream:
        ff_data = yaml.safe_load(stream)

    return ff_data


def render_ff_mixing_def(ff_data, params):
    """Render the force_field_mixing_rules.def file."""
    output = [
        "# general rule for shifted vs truncated (file generated by aiida-raspa)",
        ["truncated", "shifted"][params["shifted"]],
        "# general rule tail corrections",
        ["no", "yes"][params["tail_corrections"]],
        "# number of defined interactions",
    ]

    force_field_lines = []
    ff_mix_found = False  # If becomes True, needs to handle the mixing differently
    # TODO: this needs to be sorted for python versions where dictionaries are not sorted! #pylint: disable=fixme
    # If separate_interactions==True, prints only "none" interactions for the molecules
    for atom_type, ff_pot in ff_data["framework"][params["ff_framework"]]["atom_types"].items():
        force_field_lines.append(" ".join([str(x) for x in [atom_type] + ff_pot]))
    for molecule, ff_name in params["ff_molecules"].items():
        for atom_type, val in ff_data[molecule][ff_name]["atom_types"].items():
            if "force_field_mix" in val:
                ff_mix_found = True
                ff_pot = val["force_field_mix"]
            elif val["force_field"] == "use-framework-ff":
                continue
            else:
                ff_pot = val["force_field"]
            # In case of "separate_interactions" write the ff only if none particle
            if not params["separate_interactions"] or ff_pot[0].lower() == "none":
                force_field_lines.append(" ".join([str(x) for x in [atom_type] + ff_pot]))

    force_field_lines = check_ff_list(force_field_lines)
    output.append(len(force_field_lines))
    output.append("# atom_type, interaction, parameters")
    output.extend(force_field_lines)
    output.append("# general mixing rule for Lennard-Jones")
    output.append(params["mixing_rule"])
    string = "\n".join([str(x) for x in output]) + "\n"
    return string, ff_mix_found


def mix_molecule_ff(ff_list, mixing_rule):
    """Mix molecule-molecule interactions in case of separate_interactions: return mixed ff_list."""
    ff_mix = []
    for i, ffi in enumerate(ff_list):
        for ffj in ff_list[i:]:
            if ffi[1].lower() == ffj[1].lower() == "lennard-jones":
                eps_mix = sqrt(ffi[2] * ffj[2])
                if mixing_rule == "lorentz-berthelot":
                    sig_mix = 0.5 * (ffi[3] + ffj[3])
                elif mixing_rule == "jorgensen":
                    sig_mix = sqrt(ffi[3] * ffj[3])
                ff_mix.append(
                    "{} {} lennard-jones {:.5f} {:.5f}".format(ffi[0], ffj[0], eps_mix, sig_mix)
                )
            elif "none" in [ffi[1], ffj[1]]:
                ff_mix.append("{} {} none".format(ffi[0], ffj[0]))
            elif ffi[1].lower() == ffj[1].lower() == "feynman-hibbs-lennard-jones":
                eps_mix = sqrt(ffi[2] * ffj[2])
                if mixing_rule == "lorentz-berthelot":
                    sig_mix = 0.5 * (ffi[3] + ffj[3])
                elif mixing_rule == "jorgensen":
                    sig_mix = sqrt(ffi[3] * ffj[3])
                reduced_mass = ffi[4]  # assuming that ffi==ffj, for the moment
                ff_mix.append(
                    "{} {} feynman-hibbs-lennard-jones {:.5f} {:.5f} {:.5f}".format(
                        ffi[0], ffj[0], eps_mix, sig_mix, reduced_mass
                    )
                )
            else:
                raise NotImplementedError(
                    "FFBuilder is not able to mix different/unknown potentials."
                )
    return ff_mix


def render_ff_def(ff_data, params, ff_mix_found):
    """Render the force_field.def file."""
    output = [
        "# rules to overwrite (file generated by aiida-raspa)",
        0,
        "# number of defined interactions",
        "# mixing rules to overwrite",
        0,
    ]
    if params["separate_interactions"] or ff_mix_found:
        ff_list = []
        for molecule, ff_name in params["ff_molecules"].items():
            for atom_type, val in ff_data[molecule][ff_name]["atom_types"].items():
                ff_pot = val["force_field"]
                if ff_pot == "dummy_separate":  # Exclude molatoms-moldummy interactions
                    ff_list.append([atom_type] + ["none"])
                else:
                    ff_list.append([atom_type] + ff_pot)
        mixing_rule = params["mixing_rule"].lower()
        ff_mix = mix_molecule_ff(ff_list, mixing_rule)
        output.append(len(ff_mix))
        output.append("# type1 type2 interaction")
        output.extend(ff_mix)
    else:
        output.append(0)
    string = "\n".join([str(x) for x in output]) + "\n"
    return string  # , "force_field.def"


def render_pseudo_atoms_def(ff_data, params):
    """Render the pseudo_atoms.def file."""
    output = ["# number of pseudo atoms"]

    pseudo_atoms_lines = []
    for molecule, ff_name in params["ff_molecules"].items():
        for atom_type, val in ff_data[molecule][ff_name]["atom_types"].items():
            type_settings = val["pseudo_atom"]
            pseudo_atoms_lines.append(" ".join([str(x) for x in [atom_type] + type_settings]))

    pseudo_atoms_lines = check_ff_list(pseudo_atoms_lines)
    output.append(len(pseudo_atoms_lines))
    output.append(
        "#type print as chem oxidation mass charge polarization B-factor radii connectivity "
        + "anisotropic anisotropic-type tinker-type"
    )
    output.extend(pseudo_atoms_lines)
    string = "\n".join([str(x) for x in output]) + "\n"
    return string  # , "pseudo_atoms.def"


def render_molecule_def(ff_data, params, molecule_name):
    """Render the molecule.def file containing the thermophysical data, geometry and intramolecular force field."""
    ff_name = params["ff_molecules"][molecule_name]
    ff_dict = ff_data[molecule_name][ff_name]

    output = [
        "# critical constants: Temperature [T], Pressure [Pa], and Acentric factor [-] "
        + "(file generated by aiida-raspa)",
        ff_data[molecule_name]["critical_constants"]["tc"],
        ff_data[molecule_name]["critical_constants"]["pc"],
        ff_data[molecule_name]["critical_constants"]["af"],
    ]
    if ff_dict["atomic_positions"] == "flexible":  # read intermolecular forcefield from file
        ff_intermol_path = os.path.join(
            THISDIR, "ff_flexible", "{}_{}.def".format(molecule_name, ff_name)
        )
        with open(ff_intermol_path, "r") as ff_intermol:
            output += [line.strip() for line in ff_intermol.readlines()]
    else:  # rigid molecules: atomic positions provided as list of coordinates
        natoms = len(ff_dict["atomic_positions"])
        output.append("# Number Of atoms")
        output.append(natoms)
        output.append("# Number of groups (only whole molecule)")
        output.append(1)
        output.append("# Group-1: rigid/flexible")
        output.append("rigid")
        output.append("# Group-1: Number of atoms")
        output.append(natoms)
        output.append("# Group-1: Atomic positions")
        for i, line in enumerate(ff_dict["atomic_positions"]):
            output.append(" ".join([str(x) for x in [i] + line]))
        output.append(
            "# Chiral centers Bond  BondDipoles Bend  UrayBradley InvBend  Torsion Imp. Torsion Bond/Bond "
            + "Stretch/Bend Bend/Bend Stretch/Torsion Bend/Torsion IntraVDW IntraCoulomb"
        )
        output.append(
            " ".join([str(x) for x in [0] + [natoms - 1] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        )
        if natoms > 1:
            output.append("# Bond stretch: atom n1-n2, type, parameters")
            for i in range(1, natoms):
                output.append("0 {} RIGID_BOND".format(i))
        output.append("# Number of config moves")
        output.append(0)
    string = "\n".join([str(x) for x in output]) + "\n"
    return string


def ff_builder(params: dict) -> dict:
    """Build the force field files.

    Args:
        params (dict): Input parameters, for example:
            params = {
                # See force fields available in ff_data.yaml as framework.keys()
                'ff_framework': 'UFF',
                # See molecules available in ff_data.yaml as ff_data.keys()
                'ff_molecules': {
                    'CO2': 'TraPPE',
                # See force fields available in ff_data.yaml as {molecule}.keys()
                    'N2': 'TraPPE',
                },
                # If True shift despersion interactions, if False simply truncate them.
                'shifted': True,                    .
                # If True apply tail corrections based on homogeneous-liquid assumption
                'tail_corrections': False,
                 Options: 'Lorentz-Berthelot' or 'Jorgensen'
                'mixing_rule': 'Lorentz-Berthelot'
                 # If True use framework's force field for framework-molecule interactions
                'separate_interactions': True
            }

    Returns:
        dict: ff settings
    """
    ff_data = load_yaml()

    out_dict = {}
    out_dict["force_field_mixing_rules_def"], ff_mix_found = render_ff_mixing_def(ff_data, params)
    out_dict["force_field_def"] = render_ff_def(ff_data, params, ff_mix_found)
    out_dict["pseudo_atoms_def"] = render_pseudo_atoms_def(ff_data, params)
    for molecule_name in params["ff_molecules"]:
        out_dict["molecule_{}_def".format(molecule_name)] = render_molecule_def(
            ff_data, params, molecule_name
        )

    return out_dict
