import argparse
from typing import Optional

from ..moleculetype import Atom
from ..topfilter import TopologyFilter


def top2itp(topfile: str, moleculetypename: str, itpfile: str, posresdefine: Optional[str] = None,
            posresforce: float = 1000):
    """Convert a topol.top file made by pdb2gmx to an itp file containing just the first molecule definition

    :param topfile: name of the topology file (typically topol.top)
    :type topfile: str
    :param moleculetypename: name of the molecule type
    :type moleculetypename: str
    :param itpfile: output file name (.itp)
    :type itpfile: str
    :param posresdefine: if supplied, auto-generate a [ position_restraints ] section with the heavy atoms
    :type posresdefine: None or str
    :param posresforce: force for the position restraints (kJ/mol/nm)
    :type posresforce: float
    """
    fltr = TopologyFilter(topfile, handleifdefs=False, handleempty=False)
    moleculetype_sections_seen = False
    atoms = []
    with open(itpfile, 'wt') as fout:
        for l, comment, section, filename, lineno, line in fltr.parse():
            if l.startswith('[') and l.endswith(']') and section == 'moleculetype':
                # this is a [ moleculetype ] section
                if moleculetype_sections_seen:
                    # another moleculetype section: bail out
                    break
                moleculetype_sections_seen = True
            if section == 'system':
                break  # do not handle any more lines
            if not (l.startswith('[') and l.endswith(']')):
                if (section == 'moleculetype') and (len(l) > 0):
                    # we encountered the first line in the first [ moleculetype ] section. Note that the section header
                    # has already been written
                    line = f"{moleculetypename}        {l.split()[1]}\n"
                    moleculetype_sections_seen = True
                if (len(l) > 0) and section == 'atoms':
                    # read atoms, we will probably need them for generating position restraints
                    atoms.append(Atom.fromITPLine(l))
            if (section == 'position_restraints') and posresdefine is not None:
                # we will generate position restraints, skip this line
                line = ''
            if moleculetype_sections_seen:
                fout.write(line)  # write the line if we are in the first moleculetype section
        if posresdefine is not None:
            fout.write(f'#ifdef {posresdefine}\n')
            fout.write('[ position_restraints ]\n')
            fout.write(';atom type fx     fy     fz\n')
            for a in atoms:
                if not a.name.startswith('H'):
                    # this is not a hydrogen, create a position restraint line
                    fout.write(f'{a.index:>5d}    1 {posresforce:>6f} {posresforce:>6f} {posresforce:>6f}\n')
            fout.write('#endif\n')


def main():
    """Entry point for top2itp

    """
    parser = argparse.ArgumentParser(
        description='Convert a pdb2gmx-generated topol.top to an itp file containing a single molecule definition.',
    )
    parser.add_argument('-p', default='topol.top', help='Topology file created by gmx pdb2gmx', dest='topol',
                        action='store', required=False)
    parser.add_argument('-o', default=None, help='Output file name (*.itp)', dest='itpname', action='store',
                        required=False)
    parser.add_argument('-n', help='Molecule name', action='store', required=True, dest='molname')
    parser.add_argument('-r', help='Position restraint preprocessor macro (e.g. POSRE)', action='store', required=False,
                        dest='posresmacro', default=None)
    parser.add_argument('-f', help='Position restraint force (kJ/mol/nm)', action='store', required=False,
                        dest='posresforce', default=1000)
    parsed = parser.parse_args()
    top2itp(parsed.topol, parsed.molname,
            parsed.itpname if parsed.itpname is not None else parsed.molname.lower() + '.itp',
            posresdefine=parsed.posresmacro, posresforce=float(parsed.posresforce))
