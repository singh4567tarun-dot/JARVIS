import sys  #For command line arguments
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eye of Agamotto")
        self.resize(800, 500)

        self.cpu_label=QLabel("CPU: --%")
        self.ram_label=QLabel("RAM: --%")
        self.disk_label=QLabel("Disk: --%")

        layout=QVBoxLayout()
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.disk_label)

        container=QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__=="__main__":
    app=QApplication(sys.argv)

    window=DashboardWindow()
    window.show()

    sys.exit(app.exec())