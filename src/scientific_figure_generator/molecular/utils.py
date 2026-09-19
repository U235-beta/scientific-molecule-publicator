#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
utils.py - Shared molecular visualization utilities (SINGLE SOURCE OF TRUTH)
All CPK colors, atomic properties, and bond parsing are defined here ONLY.
Other modules import from this file; do NOT redefine these constants elsewhere.
"""

# ============================================================
# CPK color scheme (standard Corey-Pauling-Koltun)
# ============================================================
CPK_COLORS = {
    'C':  '#404040',   # Carbon - dark gray
    'H':  '#FFFFFF',   # Hydrogen - white
    'O':  '#FF0D0D',   # Oxygen - red
    'N':  '#3050F8',   # Nitrogen - blue
    'S':  '#FFFF30',   # Sulfur - yellow
    'Cl': '#1FF01F',   # Chlorine - green
    'F':  '#90E050',   # Fluorine - light green
    'P':  '#FF8000',   # Phosphorus - orange
    'B':  '#FFB5B5',   # Boron - salmon
    'Br': '#A62929',   # Bromine - dark red
    'I':  '#940094',   # Iodine - purple
    'Zn': '#7D80B0',   # Zinc - blue-gray
    'Si': '#F0C8A0',   # Silicon - tan
    'Na': '#AB5CF2',   # Sodium - purple
    'K':  '#8F40D4',    # Potassium - purple
}

# ============================================================
# Atomic properties (van der Waals radius in Angstrom, covalent radius)
# ============================================================
ATOMIC_PROPERTIES = {
    'C':  {'vdw_radius': 1.70, 'covalent_radius': 0.77, 'atomic_number': 6,  'name': 'Carbon'},
    'H':  {'vdw_radius': 1.20, 'covalent_radius': 0.37, 'atomic_number': 1,  'name': 'Hydrogen'},
    'O':  {'vdw_radius': 1.52, 'covalent_radius': 0.73, 'atomic_number': 8,  'name': 'Oxygen'},
    'N':  {'vdw_radius': 1.55, 'covalent_radius': 0.75, 'atomic_number': 7,  'name': 'Nitrogen'},
    'S':  {'vdw_radius': 1.80, 'covalent_radius': 1.02, 'atomic_number': 16, 'name': 'Sulfur'},
    'Cl': {'vdw_radius': 1.75, 'covalent_radius': 0.99, 'atomic_number': 17, 'name': 'Chlorine'},
    'F':  {'vdw_radius': 1.47, 'covalent_radius': 0.71, 'atomic_number': 9,  'name': 'Fluorine'},
    'P':  {'vdw_radius': 1.80, 'covalent_radius': 1.06, 'atomic_number': 15, 'name': 'Phosphorus'},
    'B':  {'vdw_radius': 1.65, 'covalent_radius': 0.84, 'atomic_number': 5,  'name': 'Boron'},
    'Br': {'vdw_radius': 1.85, 'covalent_radius': 1.14, 'atomic_number': 35, 'name': 'Bromine'},
    'I':  {'vdw_radius': 1.98, 'covalent_radius': 1.33, 'atomic_number': 53, 'name': 'Iodine'},
    'Zn': {'vdw_radius': 1.39, 'covalent_radius': 1.22, 'atomic_number': 30, 'name': 'Zinc'},
    'Si': {'vdw_radius': 2.10, 'covalent_radius': 1.11, 'atomic_number': 14, 'name': 'Silicon'},
}

# Default for unknown elements
DEFAULT_COLOR = '#808080'
DEFAULT_RADIUS = 0.5

def get_cpk_color(element):
    """Get CPK color for an element. SINGLE source - do not redefine."""
    return CPK_COLORS.get(element, DEFAULT_COLOR)

def get_atomic_radius(element, scale=0.4):
    """Get display radius for an atom (scaled covalent radius). SINGLE source."""
    props = ATOMIC_PROPERTIES.get(element, {'covalent_radius': DEFAULT_RADIUS})
    return props['covalent_radius'] * scale

def get_element_name(element):
    """Get full element name. SINGLE source."""
    return ATOMIC_PROPERTIES.get(element, {}).get('name', element)

# ============================================================
# Bond type constants (MOL V2000 format)
# ============================================================
BOND_SINGLE = 1
BOND_DOUBLE = 2
BOND_TRIPLE = 3
BOND_AROMATIC = 4

BOND_NAMES = {
    BOND_SINGLE: 'single',
    BOND_DOUBLE: 'double',
    BOND_TRIPLE: 'triple',
    BOND_AROMATIC: 'aromatic',
}

def get_bond_name(bond_type):
    """Get human-readable bond name. SINGLE source."""
    return BOND_NAMES.get(bond_type, f'unknown({bond_type})')

# ============================================================
# Hybridization constants
# ============================================================
HYBRID_SP = 'sp'      # 2 orbitals, 180°, linear
HYBRID_SP2 = 'sp2'    # 3 orbitals, 120°, trigonal planar + p_z
HYBRID_SP3 = 'sp3'    # 4 orbitals, 109.5°, tetrahedral

HYBRID_ANGLES = {
    HYBRID_SP:  180.0,
    HYBRID_SP2: 120.0,
    HYBRID_SP3: 109.5,
}

def get_hybrid_angle(hybridization):
    """Get bond angle for hybridization type. SINGLE source."""
    return HYBRID_ANGLES.get(hybridization, 109.5)

# ============================================================
# Chromophore classification (for autofluorescence review)
# ============================================================
CHROMOPHORES = {
    'aromatic_ring':  {'lambda_ex': (254, 380), 'lambda_em': (270, 430), 'intensity': 'strong',
                        'description': 'Benzene, naphthalene, anthracene - pi->pi* transition'},
    'ester_carbonyl': {'lambda_ex': (280, 280), 'lambda_em': (345, 370), 'intensity': 'medium',
                        'description': 'Ester C=O - n->pi* transition, weak alone'},
    'enone':           {'lambda_ex': (230, 260), 'lambda_em': (300, 380), 'intensity': 'medium',
                        'description': 'alpha,beta-unsaturated carbonyl - conjugated pi->pi*'},
    'benzoxazole':     {'lambda_ex': (370, 370), 'lambda_em': (430, 440), 'intensity': 'very strong',
                        'description': 'OB-1 optical brightener core'},
    'conjugated_diene':{'lambda_ex': (217, 450), 'lambda_em': (0, 0), 'intensity': 'variable',
                        'description': 'Red-shifts with conjugation length (+30-40nm per double bond)'},
}