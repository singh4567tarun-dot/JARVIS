import psutil
from metrics import MetricsSnapshot

def collect_metrics() -> MetricsSnapshot:
# The -> MetricsSnapshot part indicates that this function is intended to return a MetricsSnapshot object.
    cpu=psutil.cpu_percent(interval=1)
    memory=psutil.virtual_memory()
    disk=psutil.disk_usage("D:\\")

    return MetricsSnapshot(
        cpu=cpu,
        ram=memory.percent,
        disk=disk.percent
    )

if __name__=="__main__":
    snapshot=collect_metrics()

print(f"CPU: {snapshot.cpu}%")
print(f"RAM: {snapshot.ram}%")
print(f"Disk: {snapshot.disk}%")