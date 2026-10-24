import psutil
from history import HistoryBuffer
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

if __name__=="__main__":
    history=HistoryBuffer(max_samples=5)

    for i in range(8):
        snapshot=collect_metrics()
        history.add(snapshot)
        print(f"Sample {i+1}: CPU = {snapshot.cpu}%")
    print("\nStored CPU history:", list(history.cpu))

# print(f"CPU: {snapshot.cpu}%")
# print(f"RAM: {snapshot.ram}%")
# print(f"Disk: {snapshot.disk}%")