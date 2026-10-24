from collections import deque
# A deque is a collection that lets us add and remove items efficiently from wither end. Here, we're using it to keep a limited history of readings
class HistoryBuffer:
    def __init__(self, max_samples=60):
        self.cpu=deque(maxlen=max_samples)
        self.ram=deque(maxlen=max_samples)
        self.disk=deque(maxlen=max_samples)

    def add(self, snapshot):
        self.cpu.append(snapshot.cpu)
        self.ram.append(snapshot.ram)
        self.disk.append(snapshot.disk)