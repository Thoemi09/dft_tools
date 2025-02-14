
################################################################################
#
# TRIQS: a Toolbox for Research in Interacting Quantum Systems
#
# Copyright (C) 2011 by M. Ferrero, O. Parcollet
#
# DFT tools: Copyright (C) 2011 by M. Aichhorn, L. Pourovskii, V. Vildosola
#
# PLOVasp: Copyright (C) 2015 by O. E. Peil
#
# TRIQS is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# TRIQS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# TRIQS. If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
r"""
    plovasp.converter
    =================

    PLOVASP is a tool to transform raw, non-normalized
    projectors generated by VASP into normalized projectors
    corresponding to user-defined projected localized orbitals (PLO).

    Runs routines in proper order to generate and store PLOs.

    Usage: python converter.py <conf-file> [<path-to-vasp-calculation>]
"""
import sys
from . import vaspio
from .inpconf import ConfigParameters
from .elstruct import ElectronicStructure
from .plotools import generate_plo, output_as_text
import logging

# Uncomment this to get extra output
#logging.basicConfig(level=logging.DEBUG)

# Main logger from which all other loggers should be inherited
main_log = logging.getLogger('plovasp')
main_log.propagate = False

handler = logging.StreamHandler(sys.stdout)
# formatter = logging.Formatter("[%(levelname)s]:[%(name)s]: %(message)s")
formatter = logging.Formatter("[%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
main_log.addHandler(handler)


def generate_and_output_as_text(conf_filename, vasp_dir):
    """
    Parse config file, process VASP data, and store as text.
    """
# Prepare input-file parameters
    pars = ConfigParameters(conf_filename, verbosity=0)
    pars.parse_input()

# Read VASP data
    if 'efermi' in pars.general:
        efermi_required = False
    else:
        efermi_required = True
    vasp_data = vaspio.VaspData(vasp_dir, efermi_required=efermi_required)
    el_struct = ElectronicStructure(vasp_data)
    el_struct.debug_density_matrix()
    if 'efermi' in pars.general:
        el_struct.efermi = pars.general['efermi']

# Generate and store PLOs
    pshells, pgroups = generate_plo(pars, el_struct)
    output_as_text(pars, el_struct, pshells, pgroups)

def main():
    """
    This function should not be called directly but via a bash script
    'plovasp' invoking the main function as follows:

      python -m applications.dft.converters.plovasp.converter $@
    """
    narg = len(sys.argv)
    if narg < 2:
        raise SystemExit("  Usage: plovasp <conf-file> [<path-to-vasp-calcultaion>]")
    else:
        filename = sys.argv[1]
        if narg > 2:
            vasp_dir = sys.argv[2]
            if vasp_dir[-1] != '/':
                vasp_dir += '/'
        else:
            vasp_dir = './'

    generate_and_output_as_text(filename, vasp_dir)

if __name__ == '__main__':
    main()
