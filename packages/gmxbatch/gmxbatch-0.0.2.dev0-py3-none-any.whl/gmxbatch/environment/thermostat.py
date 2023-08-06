from typing import List


class Thermostat:
    ref_temperature: float
    groups: List[str]
    tau: float
    algorithm: str = 'V-rescale'

    def __init__(self, groups:List[str], ref_temperature:float, tau:float, algorithm:str='V-rescale'):
        self.groups = groups
        self.tau = tau
        self.ref_temperature = ref_temperature
        self.algorithm = algorithm
