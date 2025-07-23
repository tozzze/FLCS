from snAPI.Main import *
import pandas as pd
import matplotlib
matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt
print("Switched to:",matplotlib.get_backend())

if(__name__ == "__main__"):
    
    # select the device library
    sn = snAPI()
    # get first available device
    sn.getDevice()
    sn.setLogLevel(logLevel=LogLevel.DataFile, onOff=True)
    
    #initialize the device
    sn.initDevice(MeasMode.T3)
    
    # set the configuration for your device type
    sn.loadIniConfig("C:\\Users\\lbquy\\Downloads\\snAPI-main\\snAPI-main\\demos\\config\\PH330_Edge.ini") 
    
    sn.histogram.setRefChannel(0)
    sn.histogram.setBinWidth(1) #in picoseconds -> 2 = 0.002 sec
    sn.histogram.setNumBins(10000)
    # start histogram measurement
    sn.histogram.measure(acqTime=100000,savePTU=True) #in milliseconds -> 1000 = 1 sec, 100000 = 100 sec # can be changed
    
    # get the data
    data, bins = sn.histogram.getData()
    
    # plot the histogram
    if len(data):
        plt.clf()
        plt.plot(bins, data[1], linewidth=1.0, label='sync')
        for c in range(1, 1+sn.deviceConfig["NumChans"]):
            plt.plot(bins, data[c], linewidth=1.0, label=f'chan{c}')
        plt.xlabel('Time [ps]')
        plt.ylabel('Counts')
        plt.legend()
        plt.title("Counts / Time")
        plt.pause(0.001)

    plt.show(block=True)

    df = pd.DataFrame({'Time_ps': bins})
    for c in range(1, len(data)):
        df[f'Chan{c}'] = data[c]

    # === If using script to get IRF ===
    ##save_path = "C:\\Users\\lbquy\\Downloads\\snAPI-main\\snAPI-main\\demos\\Histo_to_csv.csv"
    #df.to_csv(save_path, index=False)
    #print(f"CSV saved to: {save_path}")

   # print(len(bins))        #should be 4096
   # print(len(data[0]))  #same
   # print(df.shape)  