import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import VoltageUnits
from snAPI.Main import *
import time

if(__name__ == "__main__"):
    # === Define scan grid ===
    x_range = np.linspace(-0.9, 0.4,60)
    y_range = np.linspace(-1,0.3,60)
    num_x = len(x_range)
    num_y = len(y_range)

    intensity_map = np.zeros((num_y, num_x))

    # === Initialize snAPI (Picoharp) ===
    sn = snAPI()
    sn.getDevice()
    sn.setLogLevel(LogLevel.DataFile, True)
    sn.initDevice(MeasMode.T3)
    sn.setLogLevel(logLevel=LogLevel.Config, onOff=True)
    sn.loadIniConfig("C:\\Users\\lbquy\\Downloads\\snAPI-main\\snAPI-main\\demos\\config\\PH330_Edge.ini")

    # Optional trigger mode setup
    numChans = sn.deviceConfig["NumChans"]
    triggerMode = TrigMode.Edge if sn.deviceConfig["SyncTrigMode"] == "Edge" else TrigMode.CFD
    if False:
        if triggerMode == TrigMode.CFD:
            sn.device.setSyncTrigMode(TrigMode.CFD)
            sn.device.setInputTrigMode(-1, TrigMode.CFD)
            sn.device.setSyncCFD(100, 0)
            sn.device.setInputCFD(-1, 100, 0)
        elif triggerMode == TrigMode.Edge:
            sn.device.setInputTrigMode(-1, TrigMode.Edge)
            sn.device.setSyncEdgeTrig(-100, 0)
            sn.device.setInputEdgeTrig(-1, -50, 0)

    sn.timeTrace.setNumBins(10000)
    sn.timeTrace.setHistorySize(11)

    # === Begin scan (no plotting inside loop) ===
    with nidaqmx.Task() as ao_task:
        ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=-10.0, max_val=10.0, units=VoltageUnits.VOLTS)
        ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao1", min_val=-10.0, max_val=10.0, units=VoltageUnits.VOLTS)

        for i, y in enumerate(y_range):
            x_seq = x_range if i % 2 == 0 else x_range[::-1]
            for j, x in enumerate(x_seq):
                x_idx = j if i % 2 == 0 else num_x - 1 - j

                print(f"[Scanning] X: {x:.3f}, Y: {y:.3f}")
                ao_task.write([x, y])

                sn.timeTrace.measure(500, waitFinished=False, savePTU=False)  # 100 ms per point
                while not sn.timeTrace.isFinished():
                    time.sleep(0.001)
                counts, times = sn.timeTrace.getData()
                cntRs = sn.getCountRates()
                chan1rate = np.sum(counts[1])
                #chan1rate = cntRs[1]
                #total_intensity = np.sum(counts[1])
                intensity_map[i, x_idx] = chan1rate

    # === Plot final heatmap ===
    plt.figure()
    plt.imshow(intensity_map, extent=[x_range[0], x_range[-1], y_range[0], y_range[-1]],
           origin='lower', aspect='auto', cmap='viridis')
    plt.colorbar(label="Integrated Intensity [cts]")
    plt.xlabel("X Voltage (V)")
    plt.ylabel("Y Voltage (V)")
    plt.title("Final Time Trace Intensity Map")
    plt.tight_layout()
    plt.show()