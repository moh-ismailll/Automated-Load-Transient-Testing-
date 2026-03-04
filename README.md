
# Automated Load Transient Test

A Python based Automated test script for load transient testing of a power distribution network is created.

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

## 🔎 Breakdown of the Python Script

### 1. Initialize VISA Resource 
The script initializes PyVISA and lists all connected instruments to identify their USB addresses.

### 2. Connect to Test Instruments
The script opens communication with:
- Power Supply (PSU)
- Electronic Load
- Oscilloscope
- Digital Multimeter (DMM)

Each instrument identity is verified using the `*IDN?` command.

### 3. Define Test Rails
A dictionary is used to store rail parameters including:
- Nominal Voltage
- Maximum Current

This structure allows scalable testing for multiple rails.

### 4. Set Input Voltage
The Power Supply Unit (PSU) is configured to provide a fixed 5V input to the DUT.

### 5. Configure Load Transient Conditions
The electronic load is configured to:
- Operate in Constant Current (CC) mode
- Step from No-Load (0A) to Full-Load (Imax)
- Trigger using a BUS command

### 6. Configure Oscilloscope Triggering
The oscilloscope is configured to:
- Use Edge Trigger mode
- Trigger on the falling edge (to capture voltage dip)
- Set trigger level at 97% of nominal voltage
- Capture waveform in Single mode

### 7. Perform Transient Measurement
The load step is triggered and the oscilloscope measures:
- Minimum voltage (Undershoot)
- Maximum voltage (Overshoot)

The measured values are compared against ±5% voltage limits to determine PASS/FAIL status.

### 8. Log Results to CSV
All rail results — including:
- Rail Name
- Undershoot
- Overshoot
- PASS/FAIL Status
- Timestamp

are saved to a CSV file for documentation and further analysis.


### 📖 Resources
- https://www.youtube.com/watch?v=1HQxnz3P9P4
- https://www.youtube.com/watch?v=TLUTCDbt52I
- https://github.com/pyvisa/pyvisa/blob/main/docs/source/introduction/example.rst
- https://iotexpert.com/pyvisa-first-use/
