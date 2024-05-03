from fractions import Fraction
from matplotlib import pyplot as plt
import matplotlib.rcsetup as st
import numpy as np
import imageio
import time
import numpy as np
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, image, width = 5, height = 5,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.


        sc = MplCanvas(self, width, height, dpi=100)
        sc.axes.imshow(image)
        self.setCentralWidget(sc)



        self.show()




def main():
    app = QtWidgets.QApplication(sys.argv)

    image = imageio.v2.imread("./testPic.jpg")
    w = MainWindow(image, width = 10, height = 10)
    app.exec_()
    print(image.shape)

    kernels = [1]
    iterations = 3
    results = []
        
    cursor = 0
    buffers = []
    buffers.append(np.zeros(image.shape))
    buffers.append(np.zeros(image.shape))
    buffers[0] = np.copy(image)

    outImage = []
    for i in range(len(image)):
        outImage.append([])
        for j in range(len(image[0])):
            outImage[i].append([0,0,0])

    print(len(buffers[0]), len(buffers[0][0]))
    for i in range(len(buffers[0])):
        for j in range(len(buffers[0][0])):
            pixel = naiveBlur(buffers[0], kernels[0], i, j, 0, iterations)
            outImage[i][j][0] = int(pixel[0]) 
            outImage[i][j][1] = int(pixel[1]) 
            outImage[i][j][2] = int(pixel[2]) 
        print("row", i, "done")

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(outImage, width = 10, height = 10)
    app.exec_()

    print("Done")









def naiveBlur(buffer, kernel, y, x, recur, maxRecur):
    red = 0
    green = 0
    blue = 0
    divisor = 0
    
    if(recur == maxRecur):
        return buffer[y][x]

    for i in range(max(y-kernel, 0), min(y+kernel+1, len(buffer))):
        for j in range(max(x-kernel, 0), min(x+kernel+1, len(buffer[0]))):
            pixel = naiveBlur(buffer, kernel, i, j, recur+1, maxRecur)
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]

            divisor += 1

    return [red/float(divisor), green/float(divisor), blue/float(divisor)]     

main()
