from tune_monitor import Tune1D, BetatronTuneMonitor, View
import asyncio
from ophyd_async.tango.core import tango_signal_r

# This should go in the controls configuration for a factory to choose the correct signal backend
controls_type: 'ophyd_async.tango.core'
host = 'localhost:11000'

# This should go in the tune monitor configuration in some way
name = 'tune_monitor'
tune_h_read_attr = 'simulator/ringsimulator/ringsimulator/Tune_h'
tune_v_read_attr = 'simulator/ringsimulator/ringsimulator/Tune_v'


# This should be done in a factory which creates the device
tune_h_read_name = f"{host}/{tune_h_read_attr}" if host else tune_h_read_attr
tune_v_read_name = f"{host}/{tune_v_read_attr}" if host else tune_v_read_attr

# This should later be read directly from a masterclock device or something simular
revolution_frequency = 0.847649e6 

# Tune for the case where the control system signal is in physics units
tune_physics = BetatronTuneMonitor(name, (tune_h_read_name, tune_v_read_name), tango_signal_r, View.PHYSICS, revolution_frequency)

async def main():
    await tune_physics.connect()
    print(f"Tune physics: {await tune_physics.read()}\n")

if __name__ == "__main__":
    asyncio.run(main())   