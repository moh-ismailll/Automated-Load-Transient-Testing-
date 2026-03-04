import pyvisa
import time
import csv
import datetime


rm = pyvisa.ResourceManager() 
print(rm.list_resources())                   # This helps to identify the instrument's address
 
psu = rm.open_resource('USB Address')        #enter actual USB addresses obtained here
eload = rm.open_resource('USB Address')
scope = rm.open_resource('USB Address')
dmm = rm.open_resource('USB Address')

print("PSU ID:", psu.query("*IDN?"))                       # Verify Instruments
print("Load ID:", eload.query("*IDN?"))
print("Scope ID:", scope.query("*IDN?"))
print("DMM ID:", dmm.query("*IDN?"))


rails = {                                               # Dictionary
    "+3V3": {"voltage": 3.3, "imax": 3.0},              # Keys
    "+1V8": {"voltage": 1.8, "imax": 3.0},
    "+3V6": {"voltage": 3.6, "imax": 2.5},
    "+2V5": {"voltage": 2.5, "imax": 1.5},
}

results = []                                           #list


for rail, params in rails.items():

    Vnom = params["voltage"]
    Imax = params["imax"]

    No_Load = 0;
    Full_Load = Imax
	
	# Set PSU to 5V input
    psu.write("VOLT 5")
    psu.write("OUTP ON")
	
	# Configure Load
    eload.write("MODE CC")                                 
    eload.write(f"CURR {No_Load}")
    eload.write(f"CURR:HIGH {Full_Load}")
    eload.write("TRIG:SOURCE BUS")
	
	# Configure Scope
    scope.write(":STOP")
    scope.write(":TRIG:MODE EDGE")
    scope.write(":TRIG:EDGE:SOUR CH1")
    scope.write(":TRIG:EDGE:SLOP NEG")
    scope.write(f":TRIG:LEV {Vnom * 0.97}")
    scope.write(":TIMEBASE:SCALE 50E-6")
    scope.write(":SINGLE")
	
	eload.write("TRIG")
    time.sleep(1)
	
	
	 # Measure Undershoot and Overshoot
    undershoot = float(scope.query(":MEAS:VMIN? CH1"))
    overshoot = float(scope.query(":MEAS:VMAX? CH1"))

    print("Vmin:", undershoot)
    print("Vmax:", overshoot)

    lower_limit = Vnom * 0.95
    upper_limit = Vnom * 1.05

    status = "PASS"
    if undershoot < lower_limit or overshoot > upper_limit:
        status = "FAIL"

    print("Status:", status)

    timestamp = datetime.datetime.now()
    results.append([rail, undershoot, overshoot, status, timestamp])

#save results to CSV

with open("load_transient_results.csv", "w", newline="") as f:                # Create CSV File
    writer = csv.writer(f)
    writer.writerow(["Rail", "Undershoot", "Overshoot", "Status", "Timestamp"])
    writer.writerows(results)

print("\nTest Complete")
