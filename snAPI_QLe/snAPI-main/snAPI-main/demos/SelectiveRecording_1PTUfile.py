import os
import time
import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import VoltageUnits
from snAPI.Main import *

if __name__ == "__main__":
    # === Scan Grid Setup ===
    x_range = np.linspace(-2, 2, 3)
    y_range = np.linspace(-2, 2, 3)
    num_x = len(x_range)
    num_y = len(y_range)

    # === Initialize snAPI (Picoharp) ===
    sn = snAPI()
    sn.getDevice()
    sn.setLogLevel(LogLevel.DataFile, True)
    sn.initDevice(MeasMode.T3)
    sn.setLogLevel(LogLevel.Config, True)
    sn.loadIniConfig("C:\\Users\\lbquy\\Downloads\\snAPI-main\\snAPI-main\\demos\\config\\PH330_Edge.ini")

    sn.timeTrace.setNumBins(10000)
    sn.timeTrace.setHistorySize(1)

    # === PTU File Setup ===
    ptu_path = "C:\\Users\\lbquy\\Downloads\\snAPI-main\\snAPI-main\\demos\\SelectiveRecording_1PTU.ptu"
    os.makedirs(os.path.dirname(ptu_path), exist_ok=True)
    if os.path.exists(ptu_path):
        os.remove(ptu_path)
    sn.setPTUFilePath(ptu_path)

    # === Start Continuous PTU Recording ===
    total_scan_time_ms = 100000  # 2 min
    sn.timeTrace.measure(total_scan_time_ms, waitFinished=False, savePTU=True)
    print(f"[INFO] Started 2-min PTU recording")

    # === Galvo Scan ===
    with nidaqmx.Task() as ao_task:
        ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=-10.0, max_val=10.0)
        ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao1", min_val=-10.0, max_val=10.0)

        for i, y in enumerate(y_range):
            x_seq = x_range if i % 2 == 0 else x_range[::-1]
            for j, x in enumerate(x_seq):
                ao_task.write([x, y])
                time.sleep(0.01)  # galvo settle

                # === 0.5s Signal Check (non-interruptive)
                sn.timeTrace.setHistorySize(1)
                time.sleep(0.5)
                counts, _ = sn.timeTrace.getData()
                max_counts = max([max(c) for c in counts])

                if max_counts >= 300000:
                    print(f"[{x:.3f},{y:.3f}]  → High signal! Staying 30s...")
                    time.sleep(30)
                else:
                    print(f"[{x:.3f},{y:.3f}]  → Low signal. Moving to next point.")
                    continue

    sn.timeTrace.stopMeasure()
    time.sleep(0.5)


    print(f"Scan complete. PTU saved at: {ptu_path}")
