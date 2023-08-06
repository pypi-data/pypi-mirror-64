from .barostat import Barostat
from .thermostat import Thermostat


class Environment:
    barostat: Barostat
    thermostat: Thermostat

    def __init__(self, thermostat: Thermostat, barostat: Barostat):
        self.thermostat = thermostat
        self.barostat = barostat
