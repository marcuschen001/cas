import sys
from PyQt5 import QtWidgets, QtGui
import cv2

from cas_ui import Ui_ContentAwareScaler
from cas import seam_carver as carver
from surprise import deep_fry as special


class MainWindow(QtWidgets.QMainWindow, Ui_ContentAwareScaler):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Different parts of the UI
        self.button = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.label1 = self.findChild(QtWidgets.QLabel, "label")
        self.label2 = self.findChild(QtWidgets.QLabel, "label_2")
        self.reset = self.findChild(QtWidgets.QPushButton, "reset")
        self.length = self.findChild(QtWidgets.QSlider, "length")
        self.width = self.findChild(QtWidgets.QSlider, "width")

        # Bonus surprise image process, treated as a boolean
        self.checkBox = self.findChild(QtWidgets.QCheckBox, "checkBox")

        # Functions for the Image Upload and Reset buttons
        self.button.clicked.connect(self.clicker)
        self.reset.clicked.connect(self.resetter)
    
    def clicker(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Upload Image", "c:\\gui\\images", "All Files(*);;PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)")
        self.pixmap = QtGui.QPixmap(fname[0])
        self.label1.setPixmap(self.pixmap)

        # Loads the image for image processing
        processing_image = cv2.imread(fname[0])
        row, col, _ = processing_image.shape

        # Content-aware scaling
        processed_image = carver(processing_image, int(self.length.value() / 100 * row), int(self.width.value() / 100 * col))

        # surprise function
        if(self.checkBox.isChecked()):
            processed_image = special(processed_image)
            
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        h, w, ch = processed_image.shape
        bytesPerLine = ch * w
        qImg = QtGui.QImage(processed_image.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)

        # Establishes the processed image to be added to the second window
        self.label2.setPixmap(QtGui.QPixmap.fromImage(qImg))
    
    # Resets the values of the length slider, width slider, and check box
    def resetter(self):
        self.length.setValue(100) 
        self.width.setValue(100) 
        self.checkBox.setChecked(False)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()