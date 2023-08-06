class Barostat:
    ref_pressure: float
    couplingtype: str
    tau: float
    compressibility: float
    algorithm: str = 'Parrinello-Rahman'

    def __init__(self, ref_pressure: float, tau: float, compressibility: float = 4.6e-5,
                 couplingtype: str = 'isotropic', algorithm: str = 'Parrinello-Rahman'):
        self.ref_pressure = ref_pressure
        self.couplingtype = couplingtype
        self.compressibility = compressibility
        self.tau = tau
        self.algorithm = algorithm

    def __repr__(self) -> str:
        return f'Barostat:\n  {self.ref_pressure:.3f}'
