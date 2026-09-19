"""
Molecular visualization subpackage.

Professional 2D/3D molecular and crystal visualization for scientific figures.
Integrates OrganicChemBuilder (RDKit.js WASM), 3Dmol (py3Dmol), and
CrystalStructure (crystal geometry algorithms).

Modules:
    utils     - CPK colors, atomic properties, bond types, hybridization (SINGLE SOURCE)
    molvis    - 2D ball-and-stick models, hybrid orbitals, electron clouds, pi orbitals, FRET
    crystal   - Crystal structure generation (10 lattices + 24 presets), bonding, physics, 2D projection
    render_3d - Interactive 3D HTML via py3Dmol (with 3Dmol.js CDN fallback)
"""

from .utils import (
    CPK_COLORS, ATOMIC_PROPERTIES, DEFAULT_COLOR, DEFAULT_RADIUS,
    get_cpk_color, get_atomic_radius, get_element_name,
    BOND_SINGLE, BOND_DOUBLE, BOND_TRIPLE, BOND_AROMATIC, get_bond_name,
    HYBRID_SP, HYBRID_SP2, HYBRID_SP3, get_hybrid_angle,
    CHROMOPHORES,
)
from .molvis import (
    load_mol, load_mol_by_name, draw_bond, draw_ball_stick,
    draw_sp_orbitals, draw_sp2_orbitals, draw_sp3_orbitals,
    draw_electron_cloud, draw_pi_orbital, draw_fret, plot_molecule,
)
from .crystal import (
    CRYSTAL_DATABASE, generate_lattice, generate_from_database,
    draw_crystal_2d, calc_unit_cell_volume, calc_packing_efficiency,
    calc_density,
)
from .render_3d import (
    mol_json_to_molblock, render_3d_html, render_multi_3d_html,
)

__all__ = [
    # utils
    "CPK_COLORS", "ATOMIC_PROPERTIES", "DEFAULT_COLOR", "DEFAULT_RADIUS",
    "get_cpk_color", "get_atomic_radius", "get_element_name",
    "BOND_SINGLE", "BOND_DOUBLE", "BOND_TRIPLE", "BOND_AROMATIC", "get_bond_name",
    "HYBRID_SP", "HYBRID_SP2", "HYBRID_SP3", "get_hybrid_angle",
    "CHROMOPHORES",
    # molvis
    "load_mol", "load_mol_by_name", "draw_bond", "draw_ball_stick",
    "draw_sp_orbitals", "draw_sp2_orbitals", "draw_sp3_orbitals",
    "draw_electron_cloud", "draw_pi_orbital", "draw_fret", "plot_molecule",
    # crystal
    "CRYSTAL_DATABASE", "generate_lattice", "generate_from_database",
    "draw_crystal_2d", "calc_unit_cell_volume", "calc_packing_efficiency",
    "calc_density",
    # render_3d
    "mol_json_to_molblock", "render_3d_html", "render_multi_3d_html",
]