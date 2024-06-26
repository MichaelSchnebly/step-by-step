import numpy as np
from OpenGL.arrays import vbo


class EventPlot:
    '''A class to store information about an Event Plot.
    -The plot is a collection of Event Lines.
    -The Event Lines are updated based on analysis of frames returned from a stream (serial port or file).
    -The Event Lines are stored as a list.
    -The Event Lines are rendered by a renderer.
    -The renderer is stored as an EventRenderer object.
    '''
    def __init__(self, n_frames):
        self.lines = [EventLines(n_frames, 0.01, np.array([0.2, 0.2,  0.2, 1]), [1, 1, 1], [0, -1, 0]), #metronome
                      EventLines(n_frames, 0.01, np.array([0.3, 0.3, 0.3, 1]), [1, 1, 1], [0, -1, 0])] #label

    def update(self, events):
        self.lines[0].update(events[0])
        self.lines[1].update(events[1])


class EventLines:
    '''A class to visually indicate events in timeseries with vertical lines.
    '''
    def __init__(self, n_frames, width = 0.002, color = np.ones(4, dtype=np.float32), scale = [1, 1, 1], translate = [0, 0, 0], running = True):
        self.x = np.linspace(-1, 1, n_frames, dtype=np.float32)
        self.vertices = np.zeros(0, dtype=np.float32)

        self.width = width
        self.color = color
        self.transform = np.eye(4, dtype=np.float32)
        self.transform = np.dot(self.transform, scaling_matrix(scale[0], scale[1], scale[2]))
        self.transform = np.dot(self.transform, translation_matrix(translate[0], translate[1], translate[2]))
    
        self.vbo = vbo.VBO(self.vertices)

        self.running = running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def update(self, events_onehot):
        if self.running:
            events = np.argwhere(events_onehot == True)
            events = events.reshape(events.shape[0])
            self.vertices = np.zeros((events.shape[0]), dtype=np.float32)
            self.vertices = self.x[events]
            self.vbo.set_array(self.vertices)

        
class NNLine:
    def __init__(self, n_frames, width = 0.002, color = np.ones(4, dtype=np.float32), scale = [1, 1, 1], translate = [0, 0, 0], running = True):
        self.vertices = np.zeros((n_frames, 3), dtype=np.float32)
        self.vertices[:, 0] = np.linspace(-1, 1, n_frames, dtype=np.float32)
        self.vertices[:, 1] = np.zeros(n_frames, dtype=np.float32)
        self.vertices[:, 2] = np.zeros(n_frames, dtype=np.float32)

        self.width = width
        self.color = color
        self.transform = np.eye(4, dtype=np.float32)
        self.transform = np.dot(self.transform, scaling_matrix(scale[0], scale[1], scale[2]))
        self.transform = np.dot(self.transform, translation_matrix(translate[0], translate[1], translate[2]))
    
        self.vbo = vbo.VBO(self.vertices)

        self.running = running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def update(self, values):
        if self.running:
            self.vertices[:, 1] = values
            self.vbo.set_array(self.vertices)

    def shift(self):
        if self.running:
            self.vertices[1:, 1] = self.vertices[:-1, 1]
            self.vertices[0, 1] = 0
            self.vbo.set_array(self.vertices)

class NNPlot:
    def __init__(self, n_frames):
        self.lines = [NNLine(n_frames, 0.006, np.array([1, 1,  1, 1]), [1, 1, 1], [0, 0, 0], False)]
    
    def update(self, values):
        self.lines[0].update(values[0])

    def shift(self):
        self.lines[0].shift()


class IMULine:
    def __init__(self, n_frames, width = 0.002, color = np.ones(4, dtype=np.float32), scale = [1, 1, 1], translate = [0, 0, 0], running = True):
        self.vertices = np.zeros((n_frames, 3), dtype=np.float32)
        self.vertices[:, 0] = np.linspace(-1, 1, n_frames, dtype=np.float32)
        self.vertices[:, 1] = np.zeros(n_frames, dtype=np.float32)
        self.vertices[:, 2] = np.zeros(n_frames, dtype=np.float32)

        self.width = width
        self.color = color
        self.transform = np.eye(4, dtype=np.float32)
        self.transform = np.dot(self.transform, scaling_matrix(scale[0], scale[1], scale[2]))
        self.transform = np.dot(self.transform, translation_matrix(translate[0], translate[1], translate[2]))
    
        self.vbo = vbo.VBO(self.vertices)

        self.running = running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def update(self, value):
        if self.running:
            self.vertices[1:, 1] = self.vertices[:-1, 1]
            self.vertices[0, 1] = value
            self.vbo.set_array(self.vertices)


class IMUPlot:
    '''A class to represent information about an IMU Plot.
        -The plot is a collection of IMU Lines.
        -The IMU Lines are updated by frames returned from a stream (serial port or file).
        -The IMU Lines are stored as a list.
        -The IMU Lines are rendered by a renderer.
        -The renderer is stored as a IMURenderer object.
    '''
    def __init__(self, n_frames):
        self.lines = [IMULine(n_frames, 0.003, np.array([0, 1,   1, 1]), [1, 1/12, 1], [0, -7/12, 0], False), #acceleration.x
                          IMULine(n_frames, 0.003, np.array([1, 0,   1, 1]), [1, 1/12, 1], [0, -9/12, 0], False), #acceleration.y
                          IMULine(n_frames, 0.003, np.array([1, 0.6, 0, 1]), [1, 1/12, 1], [0, -11/12, 0], False), #acceleration.z
                          IMULine(n_frames, 0.006, np.array([0.5, 0.5, 0.5, 1]), [1, 1/3, 1], [0, -6/12, 0], False) #acceleration.mag
                          ]
    
    def update(self, data):
        self.lines[0].update(data[0])
        self.lines[1].update(data[1])
        self.lines[2].update(data[2])
        self.lines[3].update(np.linalg.norm(data))





# Function to create a translation matrix
def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ], dtype=np.float32)

# Function to create a scaling matrix
def scaling_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


