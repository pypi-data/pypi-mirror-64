from typing import Dict

from ..conffiles import Coordinates
from ..trajectory import Trajectory
from ..xvgfile import XVGFile


class Results:
    """Container class for simulation results"""
    conf: Coordinates
    energy: Dict[str, XVGFile]
    trajectory: Trajectory
    deffnm: str

    def __init__(self, deffnm: str, conf: Coordinates, energy: Dict[str, XVGFile], trajectory: Trajectory):
        self.conf = conf
        self.energy = energy
        self.trajectory = trajectory
        self.deffnm = deffnm
