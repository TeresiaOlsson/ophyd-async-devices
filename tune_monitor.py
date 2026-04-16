from enum import Enum
from typing import Optional, Any, Callable, Tuple, TypedDict

from ophyd_async.core import StandardReadable, derived_signal_r, Transform, DerivedSignalFactory
from ophyd_async.epics.core import epics_signal_r
from ophyd_async.tango.core import tango_signal_r

class View(Enum):
    HARDWARE = "hardware"
    PHYSICS = "physics"


SignalRFactory = Callable[[type[float], str], Any]    

class TuneRaw(TypedDict):
    signal: float

class TuneDerived(TypedDict):
    frequency: float
    tune: float

class TuneTransform(Transform):
    revolution_frequency: float
    unit_factor: float
    hardware_view: bool

    def raw_to_derived(self, *, signal: float) -> TuneDerived:
        if self.hardware_view:
            frequency = signal
            tune = frequency / self.unit_factor / self.revolution_frequency
        else:
            tune = signal
            frequency = tune * self.revolution_frequency * self.unit_factor

        return TuneDerived(frequency=frequency, tune=tune)

    def derived_to_raw(self, *, frequency: float, tune: float) -> TuneRaw:
        if self.hardware_view:
            return TuneRaw(signal=frequency)
        return TuneRaw(signal=tune)


class Tune1D(StandardReadable):
    """Device to read tune in one dimension."""

    def __init__(
        self,
        name: str,
        read_name: str,
        signal_r: SignalRFactory = epics_signal_r,
        view: View = View.PHYSICS,
        revolution_frequency: float = 1.0, # This input should be removed and done in some better way
        unit_factor: float = 1.0 # This input should be removed and done in some better way
        ):

        hardware_view = view is View.HARDWARE

        if hardware_view:
            native = signal_r(float, read_name)
            self._factory = DerivedSignalFactory(
                TuneTransform,
                signal=native,
                revolution_frequency=revolution_frequency,
                hardware_view=hardware_view,
                unit_factor=unit_factor,
            )
            frequency = native
            tune = self._factory.derived_signal_r(float, "tune")
        else:
            native = signal_r(float, read_name)
            self._factory = DerivedSignalFactory(
                TuneTransform,
                signal=native,
                revolution_frequency=revolution_frequency,
                hardware_view=hardware_view,
                unit_factor=unit_factor,
            )
            tune = native
            frequency = self._factory.derived_signal_r(float, "frequency")

        with self.add_children_as_readables():
            self.frequency = frequency
            self.tune = tune

        super().__init__(name=name) 
            

class BetatronTuneMonitor(StandardReadable):

    def __init__(self,
                 name: str,
                 read_name: Tuple[str, str],
                 signal_r: SignalRFactory = epics_signal_r,
                 view: View = View.PHYSICS,
                 revolution_frequency: float = 1.0, # This input should be removed and done in some better way
                 unit_factor: float = 1.0 # This input should be removed and done in some better way
                 ):

        tune_h = Tune1D(
            "hor",
            read_name[0],
            signal_r=signal_r,
            view=view,
            revolution_frequency=revolution_frequency,
            unit_factor=unit_factor,
        )
        tune_v = Tune1D(
            "ver",
            read_name[1],
            signal_r=signal_r,
            view=view,
            revolution_frequency=revolution_frequency,
            unit_factor=unit_factor,
        )

        with self.add_children_as_readables():
            self.hor = tune_h
            self.ver = tune_v

        super().__init__(name=name)     
