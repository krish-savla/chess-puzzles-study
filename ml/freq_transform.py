#!/usr/bin/env python
# coding: utf-8

# In[15]:


import os
import pandas as pd 
import numpy as np
import mne
from library import *
from pqdm.processes import pqdm

def mne_psd_morlet(df):  
    """
    df is one puzzle's worth of data. 
    https://mne.tools/stable/auto_tutorials/time-freq/20_sensors_time_frequency.html#time-frequency-analysis-power-and-inter-trial-coherence
    """  
    data = df[CH_NAMES].values.T
    
    timestamps = df['timestamp'].values
    timestamps -= timestamps[0]
    time_diffs = np.diff(timestamps) / 1e3 # in seconds

    annotations = mne.Annotations(onset=timestamps[:-1],
                                  duration=time_diffs,
                                  description=['EDGE'] * len(time_diffs))

    info = mne.create_info(ch_names=CH_NAMES, sfreq=SAMPLING_RATE, ch_types='eeg')
    raw = mne.io.RawArray(data, info)
    raw.set_annotations(annotations)

    events = mne.make_fixed_length_events(raw, duration=1)
    epochs = mne.Epochs(raw, events, tmin=0, tmax=0.999, baseline=None)

    freqs = np.arange(1, 51)  # Frequencies from 1 to 50 Hz
    n_cycles = freqs / 2. 

    tfr = mne.time_frequency.tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, 
                                        average=False, return_itc=False, 
                                        use_fft=True)

    # convert to psd
    power = np.abs(tfr.data)**2

    # convert to log scale (bels)
    log_power = 10 * np.log10(power)

    # shape is now (n_epochs, n_channels, n_freqs, n_times)

    # Assign the dimensions to variables
    num_epochs   = log_power.shape[0]
    num_channels = log_power.shape[1]
    num_freqs    = log_power.shape[2]
    num_times    = log_power.shape[3]

    # Reshape to a 2D array (frequencies x everything else)
    power_2d = log_power.reshape(-1, num_freqs)

    # Create arrays representing the epoch, time, and channel for each row
    epochs_array   = np.repeat(np.arange(num_epochs), num_channels*num_times)
    channels_array = np.tile(np.repeat(np.arange(num_channels), num_times), num_epochs)
    times_array    = np.tile(np.arange(num_times), num_epochs*num_channels)

    # Create frequency labels for the columns
    freq_labels = [f'freq_{freq}Hz' for freq in range(num_freqs)]

    # Create a DataFrame from the power array
    df_power = pd.DataFrame(power_2d, columns=freq_labels)

    # Add these as columns to the DataFrame
    df_power['epoch']   = epochs_array
    df_power['channel'] = channels_array
    df_power['time']    = times_array



    df_power['pid']      = df.iloc[0]['pid']
    df_power['elo']      = df.iloc[0]['elo']
    df_power['elo_bin']  = df.iloc[0]['elo_bin']
    df_power['block_id'] = df.iloc[0]['block_id']
    df_power['solved']   = df.iloc[0]['solved']
    return df_power
 

if __name__ == '__main__':
    df = pd.read_csv("study_p_5_5_raw_bp_notch_avgref.csv", dtype={'pid':str})

    print(df)

    to_process = [p_p_df for  _, p_p_df in df.groupby(['pid', 'block_id'])]

    all_psd = pqdm(to_process, mne_psd_morlet, n_jobs=35)
    
    psd_df = pd.concat(all_psd).reset_index(drop=True)
    psd_df.to_csv(DBFNAME.split('.csv')[0] + '_psd_morlet' + FILTNAME, index=False)