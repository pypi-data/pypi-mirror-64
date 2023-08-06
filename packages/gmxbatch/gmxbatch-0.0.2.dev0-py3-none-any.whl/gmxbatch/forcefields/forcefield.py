import copy
import os
from typing import List, Union, Optional

from ..mdp import MDP
from ..moleculetype import MoleculeType


class ForceField:
    """Representation of a MD force field. This is a general superclass, actual force field implementations should have
    a corresponding subclass.

    Information incorporated in attributes:

    1) MDP options (`mdp`):
        The GROMACS preprocessor needs a file (.mdp) with various parameters describing the interactions, engine
        options, algorithm choices etc. Part of these are force field dependent (e.g. cut-off distances), others change
        from run to run (e.g. thermostat reference temperature or algorithm, step count, output frequency etc.).

    2) Force field name (`name`)

    3) Force field include topology file name (`itp`)

    4) Molecule types:
        GROMACS users typically employ 'pdb2gmx' to construct a topology from the coordinate set. 'gmxbatch' does not
        wrap pdb2gmx, instead requires .itp files containing [ moleculetype ] entries. Upon writing the final topology
        files (.top), these will be #include-d. Molecule types are loaded from a set of directories (`moltypespath`
        attribute, a list of strings) upon force field initialization. Since molecule types contain information on
        atom types, partial charges, etc, they typically cannot be shared between force fields.
    """
    mdp: MDP
    name: str
    itp: str
    moltypespath: List[str]
    _moleculetypes: List[MoleculeType]

    def __init__(self, itp: str, moltypespath: Union[str, List[str]]):
        """Create a new force field instance

        :param itp: include topology file name (e.g. charmm36m.ff/forcefield.itp)
        :type itp: str
        :param moltypespath: molecule types lookup directories
        :type moltypespath: list of strings (or a single string)
        """
        self.itp = itp
        self._moleculetypes = []
        self.moltypespath = [moltypespath] if isinstance(moltypespath, str) else moltypespath[:]
        self.reloadMoleculetypes()

    def reloadMoleculetypes(self):
        """Reload molecule types from the path."""
        self._moleculetypes = []
        for path in self.moltypespath:
            for filename in os.listdir(path):
                if filename.lower().endswith('.itp'):
                    print('Trying to load molecule type from {}'.format(filename))
                    try:
                        mtypes = list(MoleculeType.loadITP(
                            os.path.join(path, filename),
                            #    kind='Solute',  # ToDo: automatic recognition of molecule kinds, e.g. from the ITP file
                            #     name or from the residuetypes.dat

                        ))
                    except (RuntimeError, ValueError, OSError, FileNotFoundError):
                        raise
                    else:
                        self._moleculetypes.extend(mtypes)

    def moleculetypes(self) -> List[MoleculeType]:
        return sorted([copy.deepcopy(mt) for mt in self._moleculetypes], key=lambda mt: (mt.name, mt.itpfile))

    def moleculetype(self, name: str, count: int = 1, itpfilenamepart: Optional[str] = None) -> MoleculeType:
        """Get a molecule type instance.

        The instance is a deep copy, i.e. subsequent calls to this method give physically different objects.

        :param name: moleculetype name
        :type name: str
        :param count: the number of this molecule in your system
        :type count: int
        :param itpfilenamepart: part of the itp file name if needed for disambiguating molecule types with the same name
        :type itpfilenamepart: str or None
        :return: a molecule type instance
        :rtype: MoleculeType
        """
        # make a deep copy.
        mtypes = [mt for mt in self._moleculetypes if
                  mt.name == name and ((itpfilenamepart is None) or (itpfilenamepart in mt.itpfile))]
        if len(mtypes) > 1:
            raise ValueError(
                'Ambiguous molecule type name. Please supply a (more specific) itp file name part.')
        elif not mtypes:
            raise ValueError('Unknown molecule type')
        mt = copy.deepcopy(mtypes[0])
        mt.count = count
        return mt
