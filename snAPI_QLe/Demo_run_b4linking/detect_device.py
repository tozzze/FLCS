from snAPI.Main import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sn = snAPI()

    # Set PTU file path
    ptu_file = "C:/Data/PicoQuant/MyFileName.ptu"  # Adjust if saved elsewhere

    # Initialize PTU reader
    reader = sn.getPTUReader(ptu_file)
    photons = reader.readAllPhotons()

    # Extract resolution (in nanoseconds)
    resolution_ns = reader.header["Resolution"]  # Typically 0.004 ns for 4 ps

    # Filter photons from detector channel (exclude sync or markers)
    detector_photons = [p for p in photons if p["channel"] == 0]

    # Convert microtimes to nanoseconds
    microtimes_ns = [p["microtime"] * resolution_ns for p in detector_photons]

    # Plot lifetime histogram
    plt.figure(figsize=(8, 5))
    plt.hist(microtimes_ns, bins=200, color='blue', alpha=0.75)
    plt.xlabel("Time after Sync [ns]")
    plt.ylabel("Photon Counts")
    plt.title("Fluorescence Lifetime Histogram")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
