# Eye of Agamotto 👁️

### Real-Time System Resource Monitor

Eye of Agamotto is a Python-based desktop application that monitors
system resource utilization through a graphical dashboard. It provides
live CPU, RAM, and disk usage readings, graphical trends, battery
status, resource warning indicators, and a process-monitoring table.

The project aims to make system performance information easier to
understand through a simple, continuously updating interface.

## ✨ Features

### 1. Real-Time System Monitoring

-   **CPU Monitoring:** Displays current CPU utilization as a
    percentage.
-   **RAM Monitoring:** Displays the percentage of physical memory in
    use.
-   **Disk Monitoring:** Displays disk space utilization for the
    configured drive.
-   **Live Graphs:** Visualizes CPU, RAM, and disk usage over time using
    PyQtGraph.
-   **Automatic Updates:** Periodically refreshes resource readings
    without requiring manual input.

### 2. Battery Status Monitoring

-   Displays the current battery percentage when available.
-   Indicates whether the laptop is charging or running on battery.
-   Handles cases where battery information is unavailable.

### 3. Resource Warning Indicators

The dashboard checks resource usage against configured thresholds and
displays warnings when usage reaches the specified limits.

Default thresholds: - CPU usage: 80% - RAM usage: 80% - Disk usage: 80%

### 4. Process Monitoring

The dashboard includes a table displaying information about
resource-consuming processes.

The table contains: - **Process:** Name of the running process. - **CPU
Usage (%):** Reported CPU utilization for the process. - **Memory Usage
(%):** Percentage of total physical RAM used by the process.

Processes are sorted by CPU usage, with the highest readings displayed
first. The table is refreshed periodically.

**Note:** CPU utilization is an indicator of processing activity, not a
direct measurement of battery consumption. Per-application battery
energy usage is not currently measured by this version.

### 5. Historical Data

The application maintains a bounded history of CPU, RAM, and disk
readings for plotting.

A deque-based history buffer stores up to 60 samples per resource,
preventing historical data from growing indefinitely.

## 🛠️ Technology Stack

  Technology            Purpose
  --------------------- -------------------------------------------------------------
  Python                Application logic and system monitoring
  PySide6               Desktop graphical user interface
  PyQtGraph             Real-time resource visualization
  psutil                System metrics, battery information, and process statistics
  `collections.deque`   Bounded historical data storage
  Git and GitHub        Version control and source-code hosting

## 📁 Project Structure

EyeOfAgamotto/
├── main.py
├── dashboard.py
├── metrics.py
├── history.py
├── README.md
├── .gitignore
└── .venv/                 # Local virtual environment (not committed)

-   **`main.py`** --- Initializes the Qt application, creates the
    dashboard window, and starts the event loop.
-   **`dashboard.py`** --- Implements the GUI, resource graphs, warning
    indicators, process table, and periodic updates.
-   **`metrics.py`** --- Collects CPU, memory, disk, and battery
    information using psutil.
-   **`history.py`** --- Maintains a bounded history of resource
    measurements.
-   **`.gitignore`** --- Excludes local and generated files from version
    control.

The `.venv/` directory is created locally during setup and should not be
committed to the repository.

## ⚙️ Installation and Setup

### Prerequisites

-   Python 3.10 or later
-   Git
-   Windows is the primary development and testing environment.
-   An internet connection for installing dependencies

The project uses Python features such as type union syntax
(`float | None`), which require Python 3.10 or later.

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd EyeOfAgamotto
```

Replace the repository URL with the actual URL of your GitHub
repository.

### 2. Create a virtual environment

``` bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

``` powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the application using the
virtual environment's Python executable directly.

### 4. Install dependencies

``` bash
python -m pip install --upgrade pip
python -m pip install psutil PySide6 pyqtgraph
```

### 5. Run the application

``` bash
python main.py
```

The Eye of Agamotto desktop dashboard should open and begin displaying
resource readings.

If you prefer not to activate the virtual environment, run:

``` powershell
.\.venv\Scripts\python.exe main.py
```

## 🏗️ Architecture

The application follows a modular structure that separates data
collection, historical storage, and presentation.

1.  `main.py` starts the application.
2.  `dashboard.py` initializes the graphical interface and update
    timers.
3.  `metrics.py` collects system information and returns a
    `MetricsSnapshot`.
4.  `history.py` stores recent CPU, RAM, and disk measurements.
5.  The dashboard updates its labels and graphs using the latest
    measurements.
6.  The process-monitoring routine collects process statistics, sorts
    them by CPU utilization, and updates the table.

### Data Flow

``` text
System Operating System
          |
          v
       psutil
          |
          v
     metrics.py
          |
          v
   MetricsSnapshot
          |
          v
     dashboard.py
       /       \
      v         v
  Live GUI    history.py
  and graphs  (recent samples)

Process statistics ---> Sorted process table
```

## 📊 Implementation Details

-   Resource readings are periodically collected using Qt timers.
-   The main dashboard refreshes approximately once per second.
-   The process table uses a separate timer to avoid scanning processes
    on every graph update.
-   PyQtGraph displays historical resource measurements.
-   The history buffer retains up to 60 samples per monitored resource.
-   Process collection handles certain process-related exceptions
    because processes may terminate while being inspected.

## ⚠️ Limitations

-   **Battery attribution:** The application does not directly measure
    the exact battery consumption of individual applications.
-   **Process statistics:** CPU and memory readings can vary between
    measurements. Initial CPU readings may be zero because CPU
    utilization requires comparison between measurements.
-   **Disk monitoring:** The current implementation monitors the
    configured drive's storage capacity usage, not real-time disk
    read/write throughput.
-   **Platform support:** The project has primarily been developed and
    tested on Windows. Behavior on other operating systems has not been
    comprehensively verified.
-   **Hardware availability:** Battery information depends on what the
    operating system and hardware expose.
-   **Performance:** Process scanning and graph updates require further
    testing and optimization under different workloads.

## 🚀 Future Improvements

Potential future enhancements include:

-   More accurate per-application energy usage analysis using
    operating-system-specific energy information.
-   Low-battery warnings and estimated remaining battery time.
-   Improved process monitoring and filtering.
-   Configurable resource thresholds.
-   More detailed disk activity monitoring.
-   Improved visualization and dashboard customization.
-   Automated testing and performance optimization.
-   Broader operating-system compatibility.


## 👥 Team

**Team Name:** JARVIS

**Project:** Eye of Agamotto

## 📄 License

No license has been specified yet. A license can be added if the project
is intended for public reuse or distribution.
