import numpy as np
import math

class GestureData:
    '''A class to generate and represent gesture labels.
        -The labels are a timeseries.
        -This timeseries is updated by processing frames returned from a stream (serial port or file).
        -The timeseries is stored as a numpy array.
        -Data Indices:
            -[#, :] timepoint
            -[:, 0] no gesture
            -[:, 1] gesture
    '''
    def __init__(self, n_frames):
        self.window = 21
        self.peak_idx = self.window // 2
        self.peak_threshold = 0.5

        self.data = np.zeros(self.window, dtype=np.float32)
        self.labels = np.zeros((n_frames, 2), dtype=np.float32)
        self.labels[:, 0] = 1

        self.labeling = False

    def start_labeling(self):
        self.labeling = True

    def stop_labeling(self):
        self.labeling = False

    def update(self, data):
        self.update_data(data)
        self.update_labels()

    def update_data(self, data):
        self.data[1:] = self.data[:-1]
        self.data[0] = data

    def update_labels(self):
        self.labels[1:, :] = self.labels[:-1, :]
        self.labels[0, 0] = 1
        self.labels[0, 1] = 0

        if self.labeling:
            if self.find_peak():
                self.labels[self.peak_idx, 0] = 0
                self.labels[self.peak_idx, 1] = 1
        
        
    def find_peak(self):
        max_value = np.nanmax(self.data)

        if math.isnan(max_value):
            return False
        min_value = np.nanmin(self.data)

        if np.abs(max_value - min_value) > self.peak_threshold:
            max_idx = np.where(self.data == max_value)[0][0]

            if max_idx == self.peak_idx:
                return True

        return False