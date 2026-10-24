from collections import deque
# A deque is a collection that lets us add and remove items efficiently from wither end. Here, we're using it to keep a limited history of readings
class HistoryBuffer:
    def __init__(self, max_samples=60): # The constructor
    # By default, max_samples=60, so each history stores at most 60 readings.
    # When a 61st reading is added, the oldest one is automatically discarded. This prevents the graph history from growing indefinitely.
        self.cpu=deque(maxlen=max_samples)
        self.ram=deque(maxlen=max_samples)
        self.disk=deque(maxlen=max_samples)

    def add(self, snapshot):    #Receives a MetricsSnapshot object and adds its three values to their respective histories.
        self.cpu.append(snapshot.cpu)
        self.ram.append(snapshot.ram)
        self.disk.append(snapshot.disk)