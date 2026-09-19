#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crystal.py - Crystal structure generation and visualization
Python port of CrystalStructure repository's crystalLogic.ts (React/Three.js).
Generates lattice atoms (SC/BCC/FCC/HCP/Diamond/NaCl/CsCl/ZincBlende/Wurtzite),
molecular structures (C60/H2O/CH4), dynamic bonding, and physical calculations.

DEDUPLICATION: CPK colors and ball-and-stick drawing are imported from utils.py
and molvis.py - do NOT redefine them here. Crystal-specific functions only.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .utils import (
    CPK_COLORS, ATOMIC_PROPERTIES, get_cpk_color, get_atomic_radius,
    get_element_name, BOND_SINGLE,
)


CRYSTAL_DATABASE = {
    'Fe':  {'type': 'BCC', 'element': 'Fe', 'a': 2.866, 'name': 'Iron (alpha-Fe)'},
    'W':   {'type': 'BCC', 'element': 'W',  'a': 3.16,  'name': 'Tungsten'},
    'Cr':  {'type': 'BCC', 'element': 'Cr', 'a': 2.88,  'name': 'Chromium'},
    'Mo':  {'type': 'BCC', 'element': 'Mo', 'a': 3.15,  'name': 'Molybdenum'},
    'Ta':  {'type': 'BCC', 'element': 'Ta', 'a': 3.30,  'name': 'Tantalum'},
    'Na':  {'type': 'BCC', 'element': 'Na', 'a': 4.23,  'name': 'Sodium'},
    'K':   {'type': 'BCC', 'element': 'K',  'a': 5.23,  'name': 'Potassium'},
    'Cu':  {'type': 'FCC', 'element': 'Cu', 'a': 3.615, 'name': 'Copper'},
    'Al':  {'type': 'FCC', 'element': 'Al', 'a': 4.05,  'name': 'Aluminum'},
    'Au':  {'type': 'FCC', 'element': 'Au', 'a': 4.08,  'name': 'Gold'},
    'Ag':  {'type': 'FCC', 'element': 'Ag', 'a': 4.09,  'name': 'Silver'},
    'Ni':  {'type': 'FCC', 'element': 'Ni', 'a': 3.52,  'name': 'Nickel'},
    'Pb':  {'type': 'FCC', 'element': 'Pb', 'a': 4.95,  'name': 'Lead'},
    'Mg':  {'type': 'HCP', 'element': 'Mg', 'a': 3.21, 'c': 5.21, 'name': 'Magnesium'},
    'Ti':  {'type': 'HCP', 'element': 'Ti', 'a': 2.95, 'c': 4.68, 'name': 'Titanium'},
    'Zn':  {'type': 'HCP', 'element': 'Zn', 'a': 2.66, 'c': 4.95, 'name': 'Zinc'},
    'Co':  {'type': 'HCP', 'element': 'Co', 'a': 2.51, 'c': 4.07, 'name': 'Cobalt'},
    'C_diamond': {'type': 'Diamond', 'element': 'C', 'a': 3.57, 'name': 'Diamond'},
    'Si':        {'type': 'Diamond', 'element': 'Si', 'a': 5.43, 'name': 'Silicon'},
    'Ge':        {'type': 'Diamond', 'element': 'Ge', 'a': 5.66, 'name': 'Germanium'},
    'NaCl': {'type': 'NaCl', 'element': 'Na', 'secondary': 'Cl', 'a': 5.64, 'name': 'Sodium Chloride'},
    'CsCl': {'type': 'CsCl', 'element': 'Cs', 'secondary': 'Cl', 'a': 4.12, 'name': 'Cesium Chloride'},
    'ZnS':  {'type': 'ZincBlende', 'element': 'Zn', 'secondary': 'S', 'a': 5.41, 'name': 'Zinc Blende'},
    'Po': {'type': 'SC', 'element': 'Po', 'a': 3.35, 'name': 'Polonium'},
}


def generate_lattice(lattice_type, a=1.0, b=None, c=None, element='C',
                     secondary_element=None, alpha=90, beta=90, gamma=90):
    """Generate atom positions for a crystal lattice.
    Returns dict with 'atoms', 'bonds', 'primitive_vectors'.
    Supported: SC, BCC, FCC, HCP, Diamond, NaCl, CsCl, ZincBlende, Wurtzite, C60, H2O, CH4
    """
    b = b if b is not None else a
    c = c if c is not None else a
    atoms = []
    bonds = []

    def add_atom(pos, elem=None):
        atoms.append({'position': list(pos), 'element': elem or element})

    lt = lattice_type
    if lt == 'SC':
        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    add_atom([x*a, y*b, z*c])
    elif lt == 'BCC':
        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    add_atom([x*a, y*b, z*c])
        add_atom([a/2, b/2, c/2])
    elif lt == 'FCC':
        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    add_atom([x*a, y*b, z*c])
        add_atom([a/2, b/2, 0]); add_atom([a/2, b/2, c])
        add_atom([a/2, 0, c/2]); add_atom([a/2, b, c/2])
        add_atom([0, b/2, c/2]); add_atom([a, b/2, c/2])
    elif lt == 'Diamond':
        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    add_atom([x*a, y*b, z*c])
        add_atom([a/2, b/2, 0]); add_atom([a/2, b/2, c])
        add_atom([a/2, 0, c/2]); add_atom([a/2, b, c/2])
        add_atom([0, b/2, c/2]); add_atom([a, b/2, c/2])
        add_atom([a/4, b/4, c/4]); add_atom([3*a/4, 3*b/4, c/4])
        add_atom([a/4, 3*b/4, 3*c/4]); add_atom([3*a/4, b/4, 3*c/4])
    elif lt == 'HCP':
        radius = a
        for z in [0, c]:
            add_atom([0, 0, z])
            for i in range(6):
                angle = np.radians(i * 60)
                add_atom([radius*np.cos(angle), radius*np.sin(angle), z])
        for i in range(3):
            angle = np.radians(30 + i * 120)
            r_int = radius / np.sqrt(3)
            add_atom([r_int*np.cos(angle), r_int*np.sin(angle), c/2])
    elif lt == 'NaCl':
        s2 = secondary_element or 'Cl'
        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    add_atom([x*a, y*b, z*c], element)
        add_atom([a/2, b/2, 0], element); add_atom([a/2, b/2, c], element)
        add_atom([a/2, 0, c/2], element); add_atom([a/2, b, c/2], element)
        add_atom([0, b/2, c/2], element); add_atom([a, b/2, c/2], element)
        for pos in [[a/2,0,0],[a/2,b,0],[a/2,0,c],[a/2,b,c],
                     [0,b/2,0],[a,b/2,0],[0,b/2,c],[a,b/2,c],
                     [0,0,c/2],[a,0,c/2],[0,b,c/2],[a,b,c/2],[a/2,b/2,c/2]]:
            add_atom(pos, s2)
    elif lt == 'CsCl':
        s2 = secondary_element or 'Cl'
        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    add_atom([x*a, y*b, z*c], element)
        add_atom([a/2, b/2, c/2], s2)
    elif lt == 'ZincBlende':
        s2 = secondary_element or 'Zn'
        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    add_atom([x*a, y*b, z*c], element)
        add_atom([a/2, b/2, 0], element); add_atom([a/2, b/2, c], element)
        add_atom([a/2, 0, c/2], element); add_atom([a/2, b, c/2], element)
        add_atom([0, b/2, c/2], element); add_atom([a, b/2, c/2], element)
        add_atom([a/4, b/4, c/4], s2); add_atom([3*a/4, 3*b/4, c/4], s2)
        add_atom([a/4, 3*b/4, 3*c/4], s2); add_atom([3*a/4, b/4, 3*c/4], s2)
    elif lt == 'C60':
        phi = (1 + np.sqrt(5)) / 2
        s = a / 3.5
        coords = [
            [0,1,3*phi],[0,1,-3*phi],[0,-1,3*phi],[0,-1,-3*phi],
            [1,3*phi,0],[1,-3*phi,0],[-1,3*phi,0],[-1,-3*phi,0],
            [3*phi,0,1],[3*phi,0,-1],[-3*phi,0,1],[-3*phi,0,-1],
            [2,(1+2*phi),phi],[2,(1+2*phi),-phi],[2,-(1+2*phi),phi],[2,-(1+2*phi),-phi],
            [-2,(1+2*phi),phi],[-2,(1+2*phi),-phi],[-2,-(1+2*phi),phi],[-2,-(1+2*phi),-phi],
            [(1+2*phi),phi,2],[(1+2*phi),phi,-2],[(1+2*phi),-phi,2],[(1+2*phi),-phi,-2],
            [-(1+2*phi),phi,2],[-(1+2*phi),phi,-2],[-(1+2*phi),-phi,2],[-(1+2*phi),-phi,-2],
            [phi,2,(1+2*phi)],[phi,2,-(1+2*phi)],[phi,-2,(1+2*phi)],[phi,-2,-(1+2*phi)],
            [-phi,2,(1+2*phi)],[-phi,2,-(1+2*phi)],[-phi,-2,(1+2*phi)],[-phi,-2,-(1+2*phi)],
            [1,(2+phi),2*phi],[1,(2+phi),-2*phi],[1,-(2+phi),2*phi],[1,-(2+phi),-2*phi],
            [-1,(2+phi),2*phi],[-1,(2+phi),-2*phi],[-1,-(2+phi),2*phi],[-1,-(2+phi),-2*phi],
            [(2+phi),2*phi,1],[(2+phi),2*phi,-1],[(2+phi),-2*phi,1],[(2+phi),-2*phi,-1],
            [-(2+phi),2*phi,1],[-(2+phi),2*phi,-1],[-(2+phi),-2*phi,1],[-(2+phi),-2*phi,-1],
            [2*phi,1,(2+phi)],[2*phi,1,-(2+phi)],[2*phi,-1,(2+phi)],[2*phi,-1,-(2+phi)],
            [-2*phi,1,(2+phi)],[-2*phi,1,-(2+phi)],[-2*phi,-1,(2+phi)],[-2*phi,-1,-(2+phi)]
        ]
        for c in coords:
            add_atom([c[0]*s, c[1]*s, c[2]*s], 'C')
    elif lt == 'H2O':
        d = a / 3
        angle = np.radians(104.5)
        add_atom([0, 0, 0], 'O')
        add_atom([d, 0, 0], 'H')
        add_atom([d*np.cos(angle), d*np.sin(angle), 0], 'H')
    elif lt == 'CH4':
        s = a / 4
        add_atom([0, 0, 0], 'C')
        add_atom([s, s, s], 'H'); add_atom([s, -s, -s], 'H')
        add_atom([-s, s, -s], 'H'); add_atom([-s, -s, s], 'H')

    bond_threshold = a * 1.1
    if lt == 'BCC': bond_threshold = (np.sqrt(3)*a/2) * 1.1
    elif lt == 'FCC': bond_threshold = (np.sqrt(2)*a/2) * 1.1
    elif lt in ['Diamond', 'ZincBlende']: bond_threshold = (np.sqrt(3)*a/4) * 1.1
    elif lt == 'NaCl': bond_threshold = (a/2) * 1.1
    elif lt == 'CsCl': bond_threshold = (np.sqrt(3)*a/2) * 1.1

    for i in range(len(atoms)):
        for j in range(i+1, len(atoms)):
            p1 = np.array(atoms[i]['position'])
            p2 = np.array(atoms[j]['position'])
            dist = np.linalg.norm(p1 - p2)
            if 0.1 < dist <= bond_threshold:
                bonds.append({'from': i, 'to': j, 'distance': dist})

    primitive_vectors = None
    if lt in ['SC', 'CsCl']:
        primitive_vectors = [[a,0,0],[0,b,0],[0,0,c]]
    elif lt == 'BCC':
        primitive_vectors = [[a/2,b/2,-c/2],[-a/2,b/2,c/2],[a/2,-b/2,c/2]]
    elif lt in ['FCC', 'Diamond', 'NaCl', 'ZincBlende']:
        primitive_vectors = [[0,b/2,c/2],[a/2,0,c/2],[a/2,b/2,0]]
    elif lt in ['HCP']:
        primitive_vectors = [[a,0,0],[-a/2,a*np.sqrt(3)/2,0],[0,0,c]]

    return {
        'type': lt, 'atoms': atoms, 'bonds': bonds,
        'lattice_params': {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma},
        'primitive_vectors': primitive_vectors,
    }


def generate_from_database(name):
    """Generate a crystal from the preset database by name (e.g. 'Cu', 'NaCl', 'Si')."""
    if name not in CRYSTAL_DATABASE:
        raise ValueError(f"Unknown crystal: {name}. Available: {list(CRYSTAL_DATABASE.keys())}")
    entry = CRYSTAL_DATABASE[name]
    c = entry['c'] if 'c' in entry else None
    secondary = entry.get('secondary', None)
    return generate_lattice(entry['type'], a=entry['a'], c=c,
                            element=entry['element'], secondary_element=secondary)


def calc_unit_cell_volume(crystal):
    """Calculate unit cell volume (Angstrom^3)."""
    p = crystal['lattice_params']
    a, b, c = p['a'], p['b'], p['c']
    alpha, beta, gamma = np.radians(p['alpha']), np.radians(p['beta']), np.radians(p['gamma'])
    vol = a*b*c * np.sqrt(1 + 2*np.cos(alpha)*np.cos(beta)*np.cos(gamma)
                           - np.cos(alpha)**2 - np.cos(beta)**2 - np.cos(gamma)**2)
    return vol


def calc_theoretical_density(crystal):
    """Calculate theoretical density (g/cm^3) from atomic masses and cell volume."""
    vol_ang3 = calc_unit_cell_volume(crystal)
    vol_cm3 = vol_ang3 * 1e-24
    total_mass = 0.0
    for atom in crystal['atoms']:
        elem = atom['element']
        props = ATOMIC_PROPERTIES.get(elem, {})
        an = props.get('atomic_number', 12)
        mass = an * 1.66054e-24
        total_mass += mass
    n_atoms = len(crystal['atoms'])
    density = total_mass / vol_cm3 if vol_cm3 > 0 else 0
    return density


def calc_packing_efficiency(crystal):
    """Calculate atomic packing factor (space utilization %)."""
    vol_cell = calc_unit_cell_volume(crystal)
    vol_atoms = 0.0
    for atom in crystal['atoms']:
        elem = atom['element']
        r = ATOMIC_PROPERTIES.get(elem, {}).get('vdw_radius', 1.5)
        vol_atoms += (4/3) * np.pi * r**3
    efficiency = (vol_atoms / vol_cell * 100) if vol_cell > 0 else 0
    return min(efficiency, 100)


def draw_crystal_2d(ax, crystal, projection='xy', scale=1.0, show_unit_cell=True,
                     show_labels=False, bond_color='#888888'):
    """Draw a 2D projection of a crystal structure (ball-and-stick + unit cell)."""
    atoms = crystal['atoms']
    bonds = crystal['bonds']
    p = crystal['lattice_params']

    def project(pos):
        if projection == 'xy': return pos[0], pos[1]
        elif projection == 'xz': return pos[0], pos[2]
        else: return pos[1], pos[2]

    for bond in bonds:
        a1 = atoms[bond['from']]
        a2 = atoms[bond['to']]
        x1, y1 = project(a1['position'])
        x2, y2 = project(a2['position'])
        ax.plot([x1, x2], [y1, y2], color=bond_color, linewidth=1.5*scale,
                solid_capstyle='round', zorder=2, alpha=0.7)

    for atom in atoms:
        elem = atom['element']
        color = get_cpk_color(elem)
        r = get_atomic_radius(elem, scale=scale*0.8)
        x, y = project(atom['position'])
        ax.add_patch(Circle((x, y), r*1.15, facecolor='#222', alpha=0.2, zorder=3))
        ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor='#333',
                             linewidth=0.5, zorder=4))
        ax.add_patch(Circle((x-r*0.3, y+r*0.3), r*0.35, facecolor='white',
                             alpha=0.4, zorder=5))
        if show_labels:
            ax.text(x, y, elem, ha='center', va='center', fontsize=5*scale,
                    color='white' if elem in ['C','N','O','S'] else 'black',
                    fontweight='bold', zorder=6)

    if show_unit_cell:
        a, b, c = p['a'], p['b'], p['c']
        if projection == 'xy':
            rect = plt.Rectangle((0, 0), a, b, fill=False, edgecolor='#333',
                                  linewidth=1.5, linestyle='--', zorder=1)
        elif projection == 'xz':
            rect = plt.Rectangle((0, 0), a, c, fill=False, edgecolor='#333',
                                  linewidth=1.5, linestyle='--', zorder=1)
        else:
            rect = plt.Rectangle((0, 0), b, c, fill=False, edgecolor='#333',
                                  linewidth=1.5, linestyle='--', zorder=1)
        ax.add_patch(rect)
    ax.set_aspect('equal')


def draw_coordination_polyhedron(ax, center_pos, ligand_positions, color='#9B59B6',
                                  alpha=0.2, scale=1.0):
    """Draw a coordination polyhedron (e.g., octahedron, tetrahedron) around a central atom."""
    verts = [list(center_pos)] + [list(p) for p in ligand_positions]
    faces = []
    n = len(ligand_positions)
    for i in range(n):
        j = (i + 1) % n
        faces.append([list(center_pos), list(ligand_positions[i]), list(ligand_positions[j])])
    poly = Poly3DCollection(faces, alpha=alpha, facecolor=color, edgecolor=color, linewidth=0.5)
    ax.add_collection3d(poly)


def plot_crystal(name, projection='xy', figsize=(8, 6), save_path=None):
    """Quick plot of a crystal from the database."""
    crystal = generate_from_database(name)
    entry = CRYSTAL_DATABASE[name]
    fig, ax = plt.subplots(figsize=figsize)
    draw_crystal_2d(ax, crystal, projection=projection, show_labels=True)
    vol = calc_unit_cell_volume(crystal)
    ax.set_title(f"{entry['name']} ({crystal['type']})\n"
                 f"a={entry['a']}A, V={vol:.1f}A^3, {len(crystal['atoms'])} atoms/cell",
                 fontsize=11, fontweight='bold')
    ax.set_xlabel(f'{projection[0].upper()} (A)', fontsize=10)
    ax.set_ylabel(f'{projection[1].upper()} (A)', fontsize=10)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f'Saved: {save_path}')
    return fig, ax