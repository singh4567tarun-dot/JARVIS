from dataclasses import dataclass
# A dataclass is a convenient way to create classes primarily used to store data. Python generates methods sich as __init__() automatically.
@dataclass
class MetricsSnapshot:
    cpu: float
    ram: float
    disk: float