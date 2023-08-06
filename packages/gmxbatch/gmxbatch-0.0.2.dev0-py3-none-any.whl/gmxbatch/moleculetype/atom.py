import numpy as np


class Atom:
    """Represents an atom in a molecule

    Attributes are:
        - index: atom index (int)
        - atomtype: atom type name (str)
        - resi: residue index (int)
        - resn: residue name (str)
        - name: atom name (str)
        - cgnr: charge group index (int)
        - charge: partial charge (electronic charge unit, float)
        - mass: atomic mass (amu, float)
    """
    index: int
    atomtype: str
    resi: int
    resn: str
    name: str
    cgnr: int
    charge: float
    mass: float

    def __init__(self, index: int, atomtype: str, resi: int, resn: str, name: str, cgnr: int, charge: float,
                 mass: float):
        """Create a new Atom instance

        :param index: integer atom index
        :type index: int
        :param atomtype: atom type name
        :type atomtype: str
        :param resi: residue index
        :type resi: int
        :param resn: residue name
        :type resn: str
        :param name: atom name
        :type name: str
        :param cgnr: charge group index
        :type cgnr: int
        :param charge: partial charge (elementary charge unit)
        :type charge: float
        :param mass: atomic mass (amu)
        :type mass: float
        """
        self.index = index
        self.atomtype = atomtype
        self.resi = resi
        self.resn = resn
        self.name = name
        self.cgnr = cgnr
        self.charge = charge
        self.mass = mass

    @classmethod
    def fromITPLine(cls, line: str) -> "Atom":
        """Create a new atom from a line in an ITP file.

        :param line: line read from an itp file, in the [ atoms ] section
        :type line: str
        :return: the new Atom instance
        :rtype: Atom
        """
        linesplit = line.split(';', 1)[0].split()
        if len(linesplit) == 8:
            index, atomtype, resi, resn, name, cgnr, charge, mass = linesplit
        elif len(linesplit) == 7:
            index, atomtype, resi, resn, name, cgnr, charge = linesplit
            mass = np.nan
        else:
            raise ValueError('Invalid ITP atom line: {}'.format(line))
        return cls(index=int(index),
                   atomtype=atomtype,
                   resi=int(resi),
                   resn=resn,
                   name=name,
                   cgnr=int(cgnr),
                   charge=float(charge),
                   mass=float(mass))

    def __deepcopy__(self, memodict={}) -> "Atom":
        """Deep copy operation"""
        return Atom(self.index, self.atomtype, self.resi, self.resn, self.name, self.cgnr, self.charge, self.mass)
