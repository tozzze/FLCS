import matplotlib.pyplot as plt
import numpy as np

# === USER INPUT ===
txt_file = r"C:\Users\lbquy\Downloads\snAPI-main\snAPI-main\Demo_run_b4linking\DemoTiTrPTU.txt"
microtime_res_ps = 1         # 1 ps per unit
microtime_res_ns = 1e-3      # convert to nanoseconds
upper_gate_cutoff_ns = 100   # max time window to include in ns

# === PARSE TXT FILE ===
print("Parsing microtimes from:", txt_file)
microtimes_raw = []

with open(txt_file, 'r', encoding='utf-16le', errors='ignore') as f:
    for line in f:
        if line.startswith("CHN") or " CHN " in line:
            parts = line.strip().split()
            if len(parts) >= 5:
                try:
                    dtime = int(parts[-1])  # Last column is dtime
                    microtimes_raw.append(dtime)
                except ValueError:
                    continue

if len(microtimes_raw) == 0:
    raise RuntimeError("No valid microtime values extracted.")

print(f"Total valid microtime records: {len(microtimes_raw):,}")

# === CONVERT TO TIME IN NS AND FILTER ===
microtimes_ns = np.array(microtimes_raw) * microtime_res_ns
filtered = microtimes_ns[microtimes_ns < upper_gate_cutoff_ns]

# === PLOT LIFETIME HISTOGRAM ===
plt.figure(figsize=(8,5))
plt.hist(filtered, bins=200, color='blue', alpha=0.75, edgecolor='black')
plt.xlabel("Time [ns]")
plt.ylabel("Photon counts")
plt.title("Fluorescence Lifetime Histogram")
plt.grid(True)
plt.tight_layout()
plt.show()
