from typing import List, Optional

from .conffiles import Coordinates
from .forcefields import ForceField
from .indexgroups import IndexGroups
from .intermolecularinteractions import IntermolecularInteractions
from .moleculetype import MoleculeType
from .templating import jinjaenv


class System:
    """Represents the system studied by molecular dynamics.

    The most important attributes are:
        - conf: the current state (conformation, coordinate set etc.), instance of gmxbatch.conffiles.Coordinates
        - name: the name of this system (str)
        - moleculetypes: ordered list of MoleculeType instances: describing the kind and count of molecules
        - forcefield: force field settings (instance of ForceField)
        - indexgroups: instance of IndexGroups
        - intermolecularinteractions: instance of IntermolecularInteractions
    """
    conf: Coordinates
    name: str
    moleculetypes: List[MoleculeType]
    forcefield: ForceField
    indexgroups: IndexGroups
    intermolecularinteractions: IntermolecularInteractions

    def __init__(self, name: str, forcefield: ForceField, conf: Coordinates, moleculetypes: List[MoleculeType],
                 indexgroups: Optional[IndexGroups] = None):
        self.conf = conf
        self.name = name
        self.moleculetypes = moleculetypes
        self.forcefield = forcefield
        self.indexgroups = IndexGroups() if indexgroups is None else indexgroups
        self.intermolecularinteractions = IntermolecularInteractions()

    def writeTopology(self, topologyfile: str):
        """Write the topology file of the present state.

        :param topologyfile: file name to write the topology to.
        :type topologyfile: str
        """
        template = jinjaenv.get_template('topol.jinja2')
        with open(topologyfile, 'wt') as f:
            for chunk in template.generate(param_itp=self.forcefield.itp,
                                           moleculetypes=self.moleculetypes,
                                           systemname=self.name,
                                           moltype_itps={mt.itpfile for mt in self.moleculetypes},
                                           intermolecularinteractions=self.intermolecularinteractions):
                f.write(chunk)

    def _match_molecule(self, moltype: MoleculeType, atindex: int) -> int:
        """See how many times a molecule definition fits into a coordinate set starting at a given index

        :param moltype: molecule definition
        :type moltype: MoleculeType
        :param atindex: start index of the coordinate set
        :type atindex: int
        :return: number of matches
        :rtype: int
        """
        count = 0
        while True:
            if atindex + len(moltype.atoms) > len(self.conf.atoms):
                # molecule type is longer than the remaining atoms.
                return count
            for i, itpatom in enumerate(moltype.atoms):
                if ((itpatom.name != self.conf.atoms[atindex + i]['name']) or
                        #                        (itpatom.resi != self.conf.atoms[atindex+i]['resi']) or
                        (itpatom.resn != self.conf.atoms[atindex + i]['resn'])):
                    # mismatch found, return
                    return count
            else:
                # no mismatch found
                count += 1
                atindex += len(moltype.atoms)

    def countMolecules(self):
        """Update the topology by counting the molecules in the coordinate set.
        """
        matched_until = 0
        for mt in self.moleculetypes:
            matches = self._match_molecule(mt, matched_until)
            mt.count = matches
            matched_until += matches * len(mt.atoms)
        if matched_until < len(self.conf.atoms):
            raise ValueError('Ran out of molecule definitions while matching atoms in the coordinate set')
