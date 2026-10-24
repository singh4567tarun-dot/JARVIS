# Collect CPU, RAM, disk, battery and process information
import psutil

def collect_metrics():
# Organize functionality into a reusable function
    cpu=psutil.cpu_percent(interval=1)
    memory=psutil.virtual_memory()
    # Obtain real memory statistics
    disk=psutil.disk_usage("D:\\")

    return{
        "cpu":cpu,
        "ram": memory.percent,
        "disk": disk.percent
    }

if __name__=="__main__":
    metrics=collect_metrics()

    print(f"CPU usage: {metrics['cpu']}%")
    print(f"RAM usage: {metrics['ram']}%")
    print(f"Disk usage: {metrics['disk']}%")
