from tune_monitor import Tune1D, BetatronTuneMonitor, View
import asyncio
from ophyd_async.epics.core import epics_signal_r

# This should go in the controls configuration for a factory to choose the correct signal backend
controls_type: 'ophyd_async.epics.core'
prefix = 'a3744'

# This should go in the tune monitor configuration in some way
name = 'tune_monitor'
tune_h_read_pv = 'beam:twiss:x:tune' # Tune in physics units (this is a twin only PV)
tune_v_read_pv = 'beam:twiss:y:tune' # Tune in physics units  (this is a twin only PV)
freq_h_read_pv = 'TUNEZR:rdH' # Tune in hardware units (this is the situation in the real machine)
freq_v_read_pv = 'TUNEZR:rdV' # Tune in hardware units  (this is the situation in the real machine)


# This should be done in a factory which creates the device
tune_h_read_name = f"{prefix}:{tune_h_read_pv}" if prefix else tune_h_read_pv
tune_v_read_name = f"{prefix}:{tune_v_read_pv}" if prefix else tune_v_read_pv
freq_h_read_name = f"{prefix}:{freq_h_read_pv}" if prefix else freq_h_read_pv
freq_v_read_name = f"{prefix}:{freq_v_read_pv}" if prefix else freq_v_read_pv

# This should later be read directly from a masterclock device or something simular
revolution_frequency = 1.25e6

# Ugly temporary fix to handle that the frequency in the control system is in kHz. Should be handled properly with pint.
unit_factor = 1e-3

# Tune for the case where the control system signal is in physics units
tune_physics = BetatronTuneMonitor(name, (tune_h_read_name, tune_v_read_name), epics_signal_r, View.PHYSICS, revolution_frequency, unit_factor)

# Tune for the case where the control system signal is in hardware units
tune_hardware = BetatronTuneMonitor(name, (freq_h_read_name, freq_v_read_name), epics_signal_r, View.HARDWARE, revolution_frequency, unit_factor)

async def main():
    await tune_physics.connect()
    await tune_hardware.connect()

    print("PV in physics units:")
    print(f"Full read: {await tune_physics.read()}")
    print(f"\nHor tune: {await tune_physics.hor.tune.get_value()}")
    print(f"Ver tune: {await tune_physics.ver.tune.get_value()}")

    print("\nPV in hardware units:")
    print(f"Full read: {await tune_hardware.read()}")
    print(f"\nHor tune: {await tune_hardware.hor.frequency.get_value()}")
    print(f"Ver tune: {await tune_hardware.ver.frequency.get_value()}")

if __name__ == "__main__":
    asyncio.run(main())
