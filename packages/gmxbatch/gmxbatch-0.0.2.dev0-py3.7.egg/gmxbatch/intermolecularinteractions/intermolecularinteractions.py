from typing import List, Sequence

from .interaction import Interaction


class IntermolecularInteractions:
    """Class to represent intermolecular interactions.
    """
    interactions: List[Interaction]

    def __init__(self):
        self.interactions = []

    def addBond(self, atom1: int, atom2: int, func: int, params: Sequence[float]):
        """Add an intermolecular bond

        :param atom1: index of the 1st atom (in the coordinate set)
        :type atom1: int
        :param atom2: index of the 2nd atom (in the coordinate set)
        :type atom2: int
        :param func: function type (see GROMACS documentation)
        :type func: int
        :param params: bond parameters (see GROMACS documentation)
        :type params: sequence of floating point numbers
        """
        self.interactions.append(Interaction('bond', [atom1, atom2], func, params))

    def addAngle(self, atom1: int, atom2: int, atom3: int, func: int, params: Sequence[float]):
        """Add an intermolecular angle

        :param atom1: index of the 1st atom (in the coordinate set)
        :type atom1: int
        :param atom2: index of the 2nd atom (in the coordinate set)
        :type atom2: int
        :param atom3: index of the 3rd atom (in the coordinate set)
        :type atom3: int
        :param func: function type (see GROMACS documentation)
        :type func: int
        :param params: angle parameters (see GROMACS documentation)
        :type params: sequence of floating point numbers
        """
        self.interactions.append(Interaction('angle', [atom1, atom2, atom3], func, params))

    def addDihedral(self, atom1: int, atom2: int, atom3: int, atom4: int, func: int, params: Sequence[float]):
        """Add an intermolecular dihedral interaction

        :param atom1: index of the 1st atom (in the coordinate set)
        :type atom1: int
        :param atom2: index of the 2nd atom (in the coordinate set)
        :type atom2: int
        :param atom3: index of the 3rd atom (in the coordinate set)
        :type atom3: int
        :param atom4: index of the 4th atom (in the coordinate set)
        :type atom4: int
        :param func: function type (see GROMACS documentation)
        :type func: int
        :param params: dihedral parameters (see GROMACS documentation)
        :type params: sequence of floating point numbers
        """
        self.interactions.append(Interaction('dihedral', [atom1, atom2, atom3, atom4], func, params))

    def __str__(self) -> str:
        """String representation of the intermolecular interactions part of the topology (as it would appear in the
        topology file)"""
        if not self.interactions:
            return ''
        s = '[ intermolecular_interactions ]\n'
        bonds = [b for b in self.interactions if b.type == 'bond']
        angles = [a for a in self.interactions if a.type == 'angle']
        dihedrals = [a for a in self.interactions if a.type == 'dihedral']
        if bonds:
            s += '[ bonds ]\n'
            for b in bonds:
                s += str(b)
            s += '\n'
        if angles:
            s += '[ angles ]\n'
            for a in angles:
                s += str(a)
            s += '\n'
        if dihedrals:
            s += '[ dihedrals ]\n'
            for d in dihedrals:
                s += str(d)
            s += '\n'
        return s

    def clear(self):
        """Remove all defined intermolecular interactions
        """
        self.interactions = []
