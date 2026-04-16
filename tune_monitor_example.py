from tune_monitor import Tune1D, BetatronTuneMonitor, View
import asyncio
from ophyd_async.epics.core import epics_signal_r
from ophyd_async.tango.core import tango_signal_r


# This should go in the controls configuration
controls_type: 'epics'
prefix = 'a3744'

# This should go in the tune monitor configuration
name = 'tune_monitor'
tune_h_read_pv = 'beam:twiss:x:tune'
tune_v_read_pv = 'beam:twiss:y:tune'
freq_h_read_pv = 'TUNEZR:rdH'
freq_v_read_pv = 'TUNEZR:rdV'


# This should be done in a factory which creates the device
tune_h_read_name = f"{prefix}:{tune_h_read_pv}" if prefix else tune_h_read_pv
tune_v_read_name = f"{prefix}:{tune_v_read_pv}" if prefix else tune_v_read_pv
freq_h_read_name = f"{prefix}:{freq_h_read_pv}" if prefix else freq_h_read_pv
freq_v_read_name = f"{prefix}:{freq_v_read_pv}" if prefix else freq_v_read_pv

# This should later be read directly from a masterclock device
revolution_frequency = 1.25e6 

tune_physics = BetatronTuneMonitor(name, (tune_h_read_name, tune_v_read_name), epics_signal_r, View.PHYSICS, revolution_frequency)

tune_hardware = BetatronTuneMonitor(name, (freq_h_read_name, freq_v_read_name), epics_signal_r, View.HARDWARE, revolution_frequency)

async def main():
    await tune_physics.connect()
    await tune_hardware.connect()
    print(f"Tune physics: {await tune_physics.read()}\n")
    print(f"Tune hardware: {await tune_hardware.read()}\n")

if __name__ == "__main__":
    asyncio.run(main())    
