import sys  #gives us access to Python's system-related functionality, including command-line arguments.
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer       #A Qt class that triggers an event after a specified inteval and can repeat that event.
from metrics import collect_metrics
from history import HistoryBuffer
import pyqtgraph as pg
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
import psutil
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
DISK_THRESHOLD = 80


class DashboardWindow(QMainWindow):
    #QMainWindow is the parent class. This class inherits its functionality, including window management and setCentralWidget().

        def __init__(self):
                super().__init__()  #initializes the parent QMainWindow

                self.setWindowTitle("Eye of Agamotto")  #sets the text shown in the title bar.
                self.resize(800, 500)   # sets the initial window size to 800 pixels wide and 500 pixels tall.

        # Each QLabel displays text in your window.
                self.cpu_label=QLabel("CPU: --%")
                self.ram_label=QLabel("RAM: --%")
                self.disk_label=QLabel("Disk: --%")
                self.battery_label=QLabel("Battery: --")

                # Create the table
                self.process_table=QTableWidget(5, 3)
                self.process_table.setHorizontalHeaderLabels(
                       ["Process", "CPU Usage (%)", "Memory Usage (%)"]
                )
                self.process_table.setEditTriggers(
                       QTableWidget.EditTrigger.NoEditTriggers
                )
                self.process_table.setSelectionBehavior(
                       QTableWidget.SelectionBehavior.SelectRows
                )
                self.process_table.horizontalHeader().setStretchLastSection(True)

                self.cpu_warning=QLabel("")
                self.ram_warning=QLabel("")
                self.disk_warning=QLabel("")
        # Why use self.cpu_label instead of just cpu_label?
        # Because storing the label as an instance attribute lets other methods of your window access and update it later.
                layout=QVBoxLayout()    #Arranges widgets in a vertical column.

        # Each call to addWidget() adds a widget to the layout. Qt manages their positioning for you.

                container=QWidget() #Creates a container.
                container.setLayout(layout) #assigns the vertical layout to that container.
                self.setCentralWidget(container)    #places the container inside your main window.
        # Why do we need the container? QMainWindow has its own structure for its central area, menus, toolbars, and status bar. We put our custom layout inside a regular widget and assign that widget as the central area.
        # A container is a widget that holds other widgets. In our code, we created one using QWidget.

                self.history=HistoryBuffer(max_samples=60)

                #Refresh the dashboard every second
                self.timer=QTimer(self)
                self.timer.timeout.connect(self.update_metrics) #When the timer fires, call update_metrics() method.
                self.timer.start(1000)

                self.process_timer=QTimer(self)
                self.process_timer.timeout.connect(self.update_process_table)
                self.process_timer.start(10000)

# One limitation: metric collection and plotting still happen on the GUI thread. If we later add expensive operations, we may need to move those operations to a worker thread.

                #Create graph widgets
                self.cpu_graph=pg.PlotWidget(title="CPU Usage")
                self.cpu_graph.setMinimumHeight(180)
                self.ram_graph=pg.PlotWidget(title="RAM Usage")
                self.ram_graph.setMinimumHeight(180)
                self.disk_graph=pg.PlotWidget(title="Disk Usage")
                self.disk_graph.setMinimumHeight(180)
                #Each pg.PlotWidget creates a widget capable of displaying a graph.
                
                #Label the axes
                for graph in (self.cpu_graph, self.ram_graph, self.disk_graph):
                        graph.setLabel("left", "Usage", units="%")
                        graph.setLabel("bottom", "Time", units="seconds")
                        graph.setYRange(0, 100)
                #        graph.getAxis("left").setTicks([
                #               [(0, "0"), (20, "20"), (40, "40"),
                #                (60, "60"), (80, "80"), (100, "100")]
                #        ])
                #        graph.getAxis("left").setWidth(45)
                        left_axis=graph.getAxis("left")
                        left_axis.setWidth(45)
                        left_axis.setStyle(tickTextOffset=8)
                        left_axis.setTicks([
                               [(0, "0"),
                                (25, "25"),
                                (50, "50"),
                                (75, "75"),
                                (100, "100")]
                        ])

                        graph.showGrid(x=True, y=True, alpha=0.3)

                #Add the graphs to your layout

                layout.addWidget(self.cpu_label)
                layout.addWidget(self.cpu_graph)
                layout.addWidget(self.cpu_warning)

                layout.addWidget(self.ram_label)
                layout.addWidget(self.ram_graph)
                layout.addWidget(self.ram_warning)

                layout.addWidget(self.disk_label)
                layout.addWidget(self.disk_graph)
                layout.addWidget(self.disk_warning)

                layout.addWidget(self.battery_label)
                layout.addWidget(self.process_table)


                self.cpu_curve=self.cpu_graph.plot(pen="r")
                self.ram_curve=self.ram_graph.plot(pen="g")
                self.disk_curve=self.disk_graph.plot(pen="b")
                # We store each returned curve in an instance attribute, such as self.cpu_curve, so we can update that same curve every second.

                # NOTE: self.cpu_raph is the entire graph widget; self.cpu_curve is the line drawn inside it.

        def update_process_table(self):
                processes=[]

                for process in psutil.process_iter(['name']):
                     try:
                            cpu=process.cpu_percent(interval=None)

                            name=process.info["name"] or "Unknown"
                            if name.lower() in ("system idle process", "idle"):
                               continue
                              
                            memory=process.memory_percent()

                            processes.append((
                                   name, cpu, memory
                            ))
                     #   except (psutil.NoSuchProcess, psutil.ZombieProcess):
                     #          continue
                     #   except Exception:
                     #          continue

                     except Exception as error:
                            print("Process error: ", error)
                            continue

                processes.sort(key=lambda item: item[1], reverse=True)
                self.process_table.setRowCount(5)
                print("Processes collected: ", len(processes))

                print("Processes collected: ", len(processes))
                print("TOp processes: ", processes[:5])

                for row in range(5):
                        if row<len(processes):
                              name, cpu, memory=processes[row]

                              self.process_table.setItem(
                                     row, 0, QTableWidgetItem(name)
                              )

                              self.process_table.setItem(
                                     row, 1, QTableWidgetItem(f"{cpu:.1f}%")
                              )
                              self.process_table.setItem(
                                     row, 2, QTableWidgetItem(f"{memory:.1f}%")
                              )
                        else:
                              for column in range(3):
                                     self.process_table.setItem(
                                            row, column, QTableWidgetItem("")
                                     )
                             
                             


        def update_warnings(self, snapshot):

                if snapshot.cpu >= CPU_THRESHOLD:
                      self.cpu_warning.setText("WARNING: High CPU Usage!")
                      self.cpu_warning.setStyleSheet("color:red;")
                else:
                      self.cpu_warning.setText("")
                      self.cpu_warning.setStyleSheet("")

                if snapshot.ram >= RAM_THRESHOLD:
                      self.ram_warning.setText("WARNING: High RAM Usage!")
                      self.ram_warning.setStyleSheet("color:red;")
                else:
                      self.ram_warning.setText("")
                      self.ram_warning.setStyleSheet("")

                if snapshot.disk >= DISK_THRESHOLD:
                      self.disk_warning.setText("WARNING: High Disk Usage!")
                      self.disk_warning.setStyleSheet("color:red;")
                else:
                      self.disk_warning.setText("")
                      self.disk_warning.setStyleSheet("")

        def update_metrics(self):
                snapshot=collect_metrics()
                self.update_warnings(snapshot)
               #Store the latest readings
                self.history.add(snapshot)

                #Update the displayed values
                self.cpu_label.setText(f"CPU: {snapshot.cpu:.1f}%")
                self.ram_label.setText(f"RAM: {snapshot.ram:.1f}%")
                self.disk_label.setText(f"Disk: {snapshot.disk:.1f}%")
                #The setText() method replaces the label's current text with the new string.

                #plot stored history
                self.cpu_curve.setData(list(self.history.cpu))
                self.ram_curve.setData(list(self.history.ram))
                self.disk_curve.setData(list(self.history.disk))

                if snapshot.battery is None:
                       self.battery_label.setText("Battery: Not available")
                else:
                       status="Charging" if snapshot.plugged else "On battery"
                       self.battery_label.setText(
                              f"Battery: {snapshot.battery:.0f}% | {status}"
                       )
              #   self.update_process_table()

if __name__=="__main__":
    app=QApplication(sys.argv)  #Creates the GUI application.

    window=DashboardWindow()    #Creates an object of your custom window class and runs its initializer.
    window.show()   #makes the window visible on your screen.

    sys.exit(app.exec())    #app.exec() processes GUI events, such as clicks, repainting , and window interactions. The application continues until it exists.
# sys.exit(app.exec()) passes the applications's exit code to Python when the event loop finishes.
#Without the even loop running, Qt wouldn't be able to process timer events and refresh the dashboard automatically.