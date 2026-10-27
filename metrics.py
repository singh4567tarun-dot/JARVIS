from dataclasses import dataclass
# A dataclass is a convenient way to create classes primarily used to store data. Python generates methods sich as __init__() automatically.
import psutil
@dataclass
#With @dataclass, Python automatically generates the constructor (__init__) for you.
#Without @dataclass, you write the constructor yourself
class MetricsSnapshot:
    cpu: float
    ram: float
    disk: float
    battery: float | None
    plugged: float | None

def collect_metrics() -> MetricsSnapshot:
    cpu=psutil.cpu_percent(interval=None)
# Why interval=none? It returns a CPU percentage based on the time since the previous measurement instead of waiting for a full second. The first reading can be unreliable, so we'll take an initial sample when the dashboard starts.
    memory=psutil.virtual_memory()
    disk=psutil.disk_usage("D:\\")
    battery_info=psutil.sensors_battery()

    if battery_info is not None:
        battery=battery_info.percent
        plugged=battery_info.power_plugged
    else:
        battery=None
        plugged=None

    return MetricsSnapshot(
        cpu=cpu,
        ram=memory.percent,
        disk=disk.percent,
        battery=battery,
        plugged=plugged
    )
