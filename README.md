Examples for a tune device for EPICS and TANGO using ophyd-async.

### Installation

This is needed:

````
pip install ophyd-async[ca,tango]
pip install pytest
```

Pytest is needed because of a bug I found in the TANGO backend. I have reported it.

### BESSY II example

1. Start twin with `apptainer run oras://registry.hzdr.de/digital-twins-for-accelerators/containers/pyat-softioc-digital-twin:default-v0-5-1-bessy.2711893`

2. Run `bessy_example.py`

The output should look like:

```
PV in physics units:
Full read: {'tune_monitor-hor-tune': {'value': 0.8480722856233869, 'timestamp': 1776371174.228293, 'alarm_severity': 0}, 'tune_monitor-hor-frequency': {'value': 1060.0903570292337, 'timestamp': 1776371174.228293, 'alarm_severity': 0}, 'tune_monitor-ver-tune': {'value': 0.7267792636914973, 'timestamp': 1776371174.279716, 'alarm_severity': 0}, 'tune_monitor-ver-frequency': {'value': 908.4740796143716, 'timestamp': 1776371174.279716, 'alarm_severity': 0}}

Hor tune: 0.8480722856233869
Ver tune: 0.7267792636914973

PV in hardware units:
Full read: {'tune_monitor-hor-tune': {'value': 0.8474559579145009, 'timestamp': 1776371336.310838, 'alarm_severity': 0}, 'tune_monitor-hor-frequency': {'value': 1059.319947393126, 'timestamp': 1776371336.310838, 'alarm_severity': 0}, 'tune_monitor-ver-tune': {'value': 0.7262510844231966, 'timestamp': 1776371336.311604, 'alarm_severity': 0}, 'tune_monitor-ver-frequency': {'value': 907.8138555289958, 'timestamp': 1776371336.311604, 'alarm_severity': 0}}

Hor tune: 1059.319947393126
Ver tune: 907.8138555289958
```

### SOLEIl II example

1. Start twin with `apptainer run --cleanenv oras://gitlab-registry.synchrotron-soleil.fr/software-control-system/containers/apptainer/virtual-accelerator:latest`
`

2. Run `soleil_example.py`

The output should look like:

```
Full read: {'tune_monitor-hor-frequency': {'value': 170688.2407892475, 'timestamp': 1776371537.9916458, 'alarm_severity': tango._tango.AttrQuality.ATTR_VALID}, 'tune_monitor-hor-tune': {'value': 0.20136665151406716, 'timestamp': 1776371537.9915838, 'alarm_severity': tango._tango.AttrQuality.ATTR_VALID}, 'tune_monitor-ver-frequency': {'value': 254299.6942207392, 'timestamp': 1776371537.9917364, 'alarm_severity': tango._tango.AttrQuality.ATTR_VALID}, 'tune_monitor-ver-tune': {'value': 0.3000058918499747, 'timestamp': 1776371537.9914258, 'alarm_severity': tango._tango.AttrQuality.ATTR_VALID}}

Hor tune: 0.20136665151406716
Ver tune: 0.3000058918499747
```