"""Classes for MDP file sections"""

from typing import List, Optional


class OutputControl:
    """Represents the output control section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    nstxout: int = 5000
    nstvout: int = 5000
    nstfout: int = 5000
    nstlog: int = 5000
    nstenergy: int = 5000
    nstxout_compressed: int = 5000
    compressed_x_grps: List[str] = None

    def __init__(self, nstxout: int = 5000, nstvout: int = 5000, nstfout: int = 5000, nstlog: int = 5000,
                 nstenergy: int = 5000, nstxout_compressed: int = 5000, compressed_x_grps: Optional[List[str]] = None):
        self.nstxout = nstxout
        self.nstvout = nstvout
        self.nstfout = nstfout
        self.nstlog = nstlog
        self.nstenergy = nstenergy
        self.nstxout_compressed = nstxout_compressed
        self.compressed_x_grps = ['System'] if compressed_x_grps is None else compressed_x_grps

    def __repr__(self) -> str:
        return 'Output control:\n' + \
               f'  Coords written every {self.nstxout:d} steps\n' + \
               f'  Velocities written every {self.nstvout:d} steps\n' + \
               f'  Forces written every {self.nstfout:d} steps\n' + \
               f'  Log written every {self.nstlog:d} steps\n' + \
               f'  Energy terms written every {self.nstenergy:d} steps\n' + \
               f'  Compressed coordinates written every {self.nstxout_compressed:d} steps\n' + \
               '  Groups for writing compressed coordinates: {}\n'.format(', '.join(self.compressed_x_grps))


class NeighbourSearch:
    """Represents the neighbour search section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    cutoff_scheme: str = 'Verlet'
    nstlist: int = 20
    ns_type: str = 'grid'
    rlist: float = 1.2
    pbc: str = 'xyz'

    def __init__(self, cutoff_scheme: str = 'Verlet', nstlist: int = 20, ns_type: str = 'grid', rlist: float = 1.2,
                 pbc: str = 'xyz'):
        self.cutoff_scheme = cutoff_scheme
        self.nstlist = nstlist
        self.ns_type = ns_type
        self.rlist = rlist
        self.pbc = pbc

    def __repr__(self) -> str:
        return 'Neighbour search:\n' + \
               f'  Cut-off scheme: {self.cutoff_scheme}\n' + \
               f'  Neighbour list updated every {self.nstlist} steps\n' + \
               f'  Neighbour search algorithm: {self.ns_type}\n' + \
               f'  Neighbour search cut-off distance: {self.rlist:.4f} nm\n' + \
               f'  Periodic boundary conditions: {self.pbc}\n'


class ElectroStatics:
    """Represents the electrostatics section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    coulombtype: str = 'PME'
    coulomb_modifier: str = 'None'
    rcoulomb_switch: float = 0
    pme_order: int = 4
    fourierspacing: float = 0.16
    rcoulomb: float = 1.2

    def __init__(self, coulombtype: str = 'PME', coulomb_modifier: str = 'None', pme_order: int = 4,
                 fourierspacing: float = 0.16, rcoulomb: float = 1.2, rcoulomb_switch: float = 0.0):
        self.coulombtype = coulombtype
        self.pme_order = pme_order
        self.fourierspacing = fourierspacing
        self.rcoulomb = rcoulomb
        self.coulomb_modifier = coulomb_modifier
        self.rcoulomb_switch = rcoulomb_switch

    def __repr__(self) -> str:
        return 'Electrostatics:\n' + \
               f'  Algorithm: {self.coulombtype}\n' + \
               f'  PME order: {self.pme_order:d}\n' + \
               f'  Fourier spacing: {self.fourierspacing:.4f} 1/nm\n' + \
               f'  Cut-off distance: {self.rcoulomb:.4f} nm\n' + \
               f'  Switching distance: {self.rcoulomb_switch:.4f} nm\n' + \
               f'  Modifier: {self.coulomb_modifier}\n'


class VanderWaals:
    """Represents the Van der Waals section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    vdwtype: str = 'cutoff'
    vdw_modifier: str = 'force-switch'
    rvdw_switch: float = 1.0
    rvdw: float = 1.2
    DispCorr: str = 'no'

    def __init__(self, vdwtype: str = 'cutoff', vdw_modifier: str = 'force-switch', rvdw_switch: float = 1.0,
                 rvdw: float = 1.2, DispCorr: str = 'no'):
        self.vdwtype = vdwtype
        self.vdw_modifier = vdw_modifier
        self.rvdw_switch = rvdw_switch
        self.rvdw = rvdw
        self.DispCorr = DispCorr

    def __repr__(self) -> str:
        return 'Van der Waals interactions:\n' + \
               f'  Algorithm: {self.vdwtype}\n' + \
               f'  Modifier: {self.vdw_modifier}\n' + \
               f'  Cut-off distance: {self.rvdw:.4f}\n' + \
               f'  Switching distance: {self.rvdw_switch:.4f} nm\n' + \
               f'  Dispersion correction: {self.DispCorr}\n'


class RunControl:
    """Represents the run control section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    integrator: str = 'md'
    emtol: float = 10.0
    emstep: float = 0.01
    nstcgsteep: int = 1000
    nbfgscorr: float = 10
    dt: float = 0.002
    nsteps: int = 100000
    comm_mode: str = 'Linear'
    nstcomm: int = 100
    comm_grps: List[str] = None

    def __init__(self, integrator: str = 'md', emtol: float = 10.0, emstep: float = 0.01, nstcgsteep: int = 1000,
                 nbfgscorr: float = 10, dt: float = 0.002, nsteps: int = 100000, comm_mode: str = 'Linear',
                 nstcomm: int = 100, comm_grps: List[str] = None):
        self.integrator = integrator
        self.emtol = emtol
        self.emstep = emstep
        self.nstcgsteep = nstcgsteep
        self.nbfgscorr = nbfgscorr
        self.dt = dt
        self.nsteps = nsteps
        self.comm_mode = comm_mode
        self.nstcomm = nstcomm
        self.comm_grps = comm_grps if comm_grps is not None else []

    def __repr__(self) -> str:
        s = "Run control:\n" + \
            f'  Integrator: {self.integrator}\n' + \
            f'  Number of steps: {self.nsteps}\n'

        if self.integrator == 'steep':
            s += \
                f'  Maximum force tolerance: {self.emtol:.4f} kJ/mol/nm\n' + \
                f'  Minimization step size: {self.emstep:.4f} nm\n'
        elif self.integrator == 'cg':
            f'  Maximum force tolerance: {self.emtol:.4f} kJ/mol/nm\n' + \
            f'  Minimization step size: {self.emstep:.4f} nm\n' + \
            f'  Steepest descent step performed at every {self.nstcgsteep:d} conj-grad. steps\n'
        elif self.integrator == 'l-bfgs':
            f'  Maximum force tolerance: {self.emtol:.4f} kJ/mol/nm\n' + \
            f'  Minimization step size: {self.emstep:.4f} nm\n' + \
            f'  Number of correction steps: {self.nbfgscorr:d}\n'
        elif self.integrator == 'md':
            f'  Time step: {self.dt:.4f} ps\n' + \
            f'  Center-of-mass motion removal: {self.comm_mode}\n' + \
            f'  Center-of-mass groups: {", ".join(self.comm_grps)}\n' + \
            f'  Center-of-mass motion zeroed every {self.nstcomm} steps\n'
        else:
            raise ValueError('Unknown integrator {}'.format(self.integrator))
        return s


class Thermostat:
    """Represents the thermostat section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    tcoupl: str = 'V-rescale'
    nsttcouple: int = -1
    tc_grps: List[str] = None
    tau_t: List[float] = None
    ref_t: List[float] = None

    def __init__(self, tcoupl: str = 'V-rescale', nsttcouple: int = -1, tc_grps: List[str] = None,
                 tau_t: List[float] = None, ref_t: List[float] = None):
        self.tcoupl = tcoupl
        self.nsttcouple = nsttcouple
        self.tc_grps = tc_grps if tc_grps is not None else ['System']
        self.tau_t = tau_t if tau_t is not None else [1.0]
        self.ref_t = ref_t if ref_t is not None else [300.0]

    def __repr__(self) -> str:
        return 'Thermostat:\n' + \
               f'  Algorithm: {self.tcoupl}\n' + \
               (
                   f'  Temperature coupling performed every {self.nsttcouple} steps\n'
                   if self.nsttcouple > 0
                   else '  Temperature coupling performed upon every neighbour list update\n') + \
               f'  Groups: {", ".join(["{}({:.2f} K, tau={:.2f} ps)".format(g, t,tau) for g, t,tau in zip(self.tc_grps, self.ref_t, self.tau_t)])}\n'


class Barostat:
    """Represents the barostat section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    pcoupl: str = 'Berendsen'
    pcoupltype: str = 'isotropic'
    nstpcouple: int = -1
    tau_p: float = 1
    ref_p: List[float]
    compressibility: List[float]
    refcoord_scaling: str = 'com'

    def __init__(self, pcoupl: str = 'Berendsen', pcoupltype: str = 'isotropic', nstpcouple: int = -1, tau_p: float = 1,
                 ref_p: List[float] = None, compressibility: List[float] = None, refcoord_scaling: str = 'com'):
        self.pcoupl = pcoupl
        self.pcoupltype = pcoupltype
        self.nstpcouple = nstpcouple
        self.tau_p = tau_p
        self.ref_p = ref_p if ref_p is not None else [1.0]
        self.compressibility = compressibility if compressibility is not None else [4.6e-5]
        self.refcoord_scaling = refcoord_scaling

    def __repr__(self) -> str:
        return 'Barostat:\n' + \
               f'  Coupling algorithm: {self.pcoupl}\n' + \
               f'  Coupling type: {self.pcoupltype}\n' + \
               (
                   f'  Pressure coupling performed every {self.nstpcouple} steps\n'
                   if self.nstpcouple > 0
                   else '  Pressure coupling performed upon every neighbour list update\n') + \
               f'  Time constant: {self.tau_p:.4f} ps\n' + \
               f'  Reference pressure(s): {", ".join(["{:.2f} bar".format(p) for p in self.ref_p])}\n' + \
               f'  Compressibility(s): {", ".join("{:.5g} 1/bar".format(c) for c in self.compressibility)}\n' + \
               f'  Reference coordinate scaling mode: {self.refcoord_scaling}\n'


class VelocityGeneration:
    """Represents the velocity generation section of the MDP file. For the documentation of the attributes, see the
    GROMACS Reference Manual."""
    gen_vel: bool = False
    gen_temp: float = 300
    gen_seed: int = -1

    def __init__(self, gen_vel: bool = False, gen_temp: float = 300, gen_seed: int = -1):
        self.gen_vel = gen_vel
        self.gen_temp = gen_temp
        self.gen_seed = gen_seed

    def __repr__(self) -> str:
        if self.gen_vel:
            return "Velocity generation:\n" + \
                   f'  Reference temperature: {self.gen_temp:.2f} K\n' + \
                   f'  Random seed: {self.gen_seed:d}\n'
        else:
            return "Velocity generation disabled.\n"


class Constraints:
    """Represents the constraints section of the MDP file. For the documentation of the attributes, see the GROMACS
    Reference Manual."""
    constraints: str = 'none'
    constraint_algorithm: str = 'LINCS'
    continuation: bool = False
    lincs_order: int = 4
    lincs_iter: int = 1

    def __init__(self, constraints: str = 'none', constraint_algorithm: str = 'LINCS', continuation: bool = False,
                 lincs_order: int = 4, lincs_iter: int = 1):
        self.constraints = constraints
        self.constraint_algorithm = constraint_algorithm
        self.continuation = continuation
        self.lincs_order = lincs_order
        self.lincs_iter = lincs_iter

    def __repr__(self) -> str:
        return "Constraints:\n" + \
               f'  Bond to constraint mode: {self.constraints}\n' + \
               f'  Algorithm: {self.constraint_algorithm}\n' + \
               f'  Continue from previous run: {self.continuation}\n' + \
               f'  LINCS order: {self.lincs_order}\n' + \
               f'  LINCS iterations: {self.lincs_iter}\n'
