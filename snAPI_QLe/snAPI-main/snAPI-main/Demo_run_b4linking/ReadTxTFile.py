import os

# === USER INPUT ===
txt_path = r"C:\Users\lbquy\Downloads\snAPI-main\snAPI-main\Demo_run_b4linking\DemoTiTrPTU.txt"

# === PREVIEW FIRST PHOTON EVENTS ===
if not os.path.exists(txt_path):
    raise FileNotFoundError(f"TXT file not found: {txt_path}")

print("Preview of CHN lines from TXT file:")
with open(txt_path, "r", encoding="utf-16le") as f:
    chn_lines = [line.strip() for line in f if "CHN" in line]
    for i, line in enumerate(chn_lines[:20]):
        print(f"{i+1}: {line}")

print(f"\nTotal CHN records found: {len(chn_lines)}")
