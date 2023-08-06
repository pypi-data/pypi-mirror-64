from typing import Sequence, Tuple


class Interaction:
    atoms: Tuple[int, ...]
    func: int
    parameters: Tuple[float, ...]
    type: str

    def __init__(self, type: str, atoms: Sequence[int], functype: int, parameters: Sequence[float]):
        self.type = type
        if type == 'bond' and len(atoms) != 2:
            raise ValueError('Bonds need two atoms.')
        elif type == 'angle' and len(atoms) != 3:
            raise ValueError('Angles need three atoms.')
        elif type == 'dihedral' and len(atoms) != 4:
            raise ValueError('Dihedrals need four atoms.')
        self.atoms = tuple(atoms)
        self.func = functype
        self.parameters = tuple(parameters)

    def __str__(self) -> str:
        return ' '.join(['{:>7d}'.format(a) for a in self.atoms]) + f' {self.func:>5d}  ' + '   '.join(
            [str(p) for p in self.parameters]) + '\n'
