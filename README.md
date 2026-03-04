
# Automated Load Transient Test

A Python_based Automated test script for load transient testing of the power distribution network is created.

### Instruments used:

1. Programmable DC Power Supply - Keithley 2230-30-1
2. Programmable Electronic Load -  Keithley 2380 Series
3. Oscilloscope - Keysight DSOX6004A
4. Digital Multimeter - Keithley DMM6500


### Test Parameters

| Rail Name | Nominal Voltage (V) | Tolerance | Max Current (A) |
|-----------|---------------------|------------|-----------------|
| +3V6      | 3.6                 | ±5%        | 2.5             |
| +1V8      | 1.8                 | ±5%        | 3.0             |
| +3V3      | 3.3                 | ±5%        | 3.0             |
| +2V5      | 2.5                 | ±5%        | 1.5             |


### PyVISA
PyVISA is an open-source Python package that enables easy control of measurement instruments and test equipment (oscilloscopes, multimeters, power supplies) via GPIB, RS232, USB, and Ethernet. It acts as a wrapper for the Virtual Instrument Software Architecture (VISA) standard, allowing Python scripts to communicate with devices across Windows, Linux, and macOS. 

### Breakdown of the Python Script

1. Initialize VISA Resource Manager: The script initializes PyVISA and lists all connected instruments to identify their USB addresses.

2. Connect to Test Instruments, It opens communication with:
Power Supply (PSU),
Electronic Load,
Oscilloscope,
Digital Multimeter (DMM).

3. Instrument identity is verified using *IDN?.

4. Define Test Rails: A dictionary stores rail parameters including:
[Nominal voltage,
Maximum current]

5. Set Input Voltage: The PSU is configured to provide a fixed 5V input to the DUT.

6. Configure Load Transient Conditions: The electronic load is set to Constant Current (CC) mode.

--> Step from No-Load (0A) to Full-Load (Imax)

-->Triggered via BUS command

7. Configure Oscilloscope: Triggering The oscilloscope is configured to:

--> Use edge trigger mode

--> Trigger on falling edge (to capture voltage dip)

--> Set trigger level at 97% of nominal voltage

--> Capture waveform in single mode

8. Perform Transient Measurement: The load step is triggered and the oscilloscope measures:

--> Minimum voltage (undershoot)

--> Maximum voltage (overshoot)

The results are compared against ±5% limits.

9. Log Results to CSV:

--> All rail results (including PASS/FAIL status and timestamp) are saved to a CSV file for documentation and analysis.