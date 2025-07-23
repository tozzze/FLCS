import os
import time
import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import VoltageUnits
from snAPI.Main import *

if __name__ == "__main__":
    # === Scan Grid Setup ===
    x_range = np.linspace(-2, 2, 2)   #moving galvo x-axis
    y_range = np.linspace(-2, 2, 2)    #moving galvo y-axis
    num_x = len(x_range)
    num_y = len(y_range)
    intensity_map = np.zeros((num_y, num_x))

    # === Initialize snAPI (Picoharp) ===
    sn = snAPI()
    sn.getDevice()
    sn.setLogLevel(LogLevel.DataFile, True)
    sn.initDevice(MeasMode.T3)
    sn.setLogLevel(LogLevel.Config, True)
    sn.loadIniConfig("C:\\Users\\lbquy\\Downloads\\snAPI-main\\snAPI-main\\demos\\config\\PH330_Edge.ini") ##If using CFD mode, change Ini file to PH330_CFD.ini

    # === Trigger setup (optional) ===
    numChans = sn.deviceConfig["NumChans"]
    triggerMode = TrigMode.Edge if sn.deviceConfig["SyncTrigMode"] == "Edge" else TrigMode.CFD

    if False:  # Change to True if you want to override config.ini
        if triggerMode == TrigMode.CFD:
            sn.device.setSyncTrigMode(TrigMode.CFD)
            sn.device.setInputTrigMode(-1, TrigMode.CFD)
            sn.device.setSyncCFD(100, 0)
            sn.device.setInputCFD(-1, 100, 0)
        else:
            sn.device.setInputTrigMode(-1, TrigMode.Edge)
            sn.device.setSyncEdgeTrig(-100, 0)
            sn.device.setInputEdgeTrig(-1, -50, 0)

    sn.timeTrace.setNumBins(10000)
    sn.timeTrace.setHistorySize(1)

    # === PTU File Setup ===
    ptu_path = "C:\\Users\\lbquy\\Downloads\\snAPI-main\\snAPI-main\\demos\\SelectiveRecording_File.ptu"
    os.makedirs(os.path.dirname(ptu_path), exist_ok=True)
    if os.path.exists(ptu_path):
        os.remove(ptu_path)
    sn.setPTUFilePath(ptu_path)

    # === Start Scan ===
    with nidaqmx.Task() as ao_task:
        ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=-10.0, max_val=10.0, units=VoltageUnits.VOLTS)
        ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao1", min_val=-10.0, max_val=10.0, units=VoltageUnits.VOLTS)

        for i, y in enumerate(y_range):
            x_seq = x_range if i % 2 == 0 else x_range[::-1]
            for j, x in enumerate(x_seq):
                x_idx = j if i % 2 == 0 else num_x - 1 - j
                #print(f"\n[Scanning] X: {x:.3f}, Y: {y:.3f}")
                ao_task.write([x, y])

                # === Initial 0.5s check ===
                sn.timeTrace.measure(500, waitFinished=False, savePTU=False) #the number can be changed 
                while not sn.timeTrace.isFinished():
                    time.sleep(0.001)
                counts, times = sn.timeTrace.getData()
                max_counts = max([max(c) for c in counts])
                #chan1_counts = counts[1]

                if max_counts >= 100000:  ##counts threshold, the number can be changed
                    print("  → High signal! Continuing 10s recording...")
                    sn.timeTrace.measure(10000, waitFinished=False, savePTU=True)  #time hold to collect at each point #time is in milisecond #the number can be changed
                    while not sn.timeTrace.isFinished():
                        time.sleep(0.1)
                    print("  → 30s data recorded.")
                else:
                    print("  → Low signal. Skipping long recording.")