'''
 Copyright (c) 2020, UChicago Argonne, LLC
 See LICENSE file.
'''
import numpy as np
import PyQt5.QtWidgets as qtWidgets
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.ROI import RectROI

import logging
from PyQt5.Qt import QPoint, QRectF
from pyqtgraph.widgets.HistogramLUTWidget import HistogramLUTWidget
from matplotlib import cm
logger = logging.getLogger(__name__)
class ImageView(qtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        layout = qtWidgets.QVBoxLayout()
        self.roi = None
        self.fx1 = 0
        self.fx2 = 0
        self.fy1 = 0
        self.fy2 = 0
        sectionLabel = qtWidgets.QLabel("Sum of Data for Crystal")
        graphicsWidget = GraphicsLayoutWidget()
        self.viewBox = graphicsWidget.addViewBox()
        self.viewBox.setAspectLocked(True)
        self.viewBox.setVisible(False)
        self.viewBox.show()
        self.imageView = ImageItem(border={'color':'333'})
        self.imageView.setOpts(axisOrder='row-major')
        
        self.viewBox.addItem(self.imageView)
        self.viewBox.show()
        layout.addWidget(sectionLabel)
        layout.addWidget(graphicsWidget)
        self.setLayout(layout)
        
        self.histWidget = HistogramLUTWidget(image=self.imageView)
        colormap = cm.get_cmap("Greys_r")
        colormap._init()
        lut = (colormap._lut* 255).view(np.ndarray)
        self.imageView.setLookupTable(lut)
        self.histWidget.item.setImageItem(self.imageView)
        self.imageView.scene().sigMouseMoved.connect(self.handleMouseMoved)

    def handleMouseMoved(self, viewPos):
        scenePos = self.imageView.mapFromScene(viewPos)
        mainWindow = self.window()
        row, col = int(scenePos.y()), int(scenePos.x())
        image = self.imageView.image
        if (not image is None) and \
            ((0<=row < image.shape[0]) and (0<= col <image.shape[1])) :
            mainWindow.statusBar().showMessage("x=%s, y=%s val=%s"
                                                %(col+self.fx1,row+self.fy1, self.imageView.image[row, col]))
        else:
            mainWindow.statusBar().showMessage("")
            
        
    def setImage(self, image, xtal, autoRange=True):
        self.imageView.setImage(image,autoLevels=False)
        #self.viewBox.autoRange(items=[self.imageView,])
#        self.imageView.setRect(QRectF(xtal[0][0], xtal[1][0], xtal[0][1], xtal[1][1]))
#         if autoRange:
#             self.viewBox.autoRange(items=[self.imageView,])
        if not self.roi is None:
            self.viewBox.removeItem(self.roi)
            self.roi = None
        #self.imageView.update()
        
    def setROI(self, crystalBounds, fileCrystalBounds):
        x1 = int(crystalBounds[0][0])
        x2 = int(crystalBounds[1][0])
        y1 = int(crystalBounds[0][1])
        y2 = int(crystalBounds[1][1])
        self.fx1 = int(fileCrystalBounds[0][0])
        self.fy1 = int(fileCrystalBounds[0][1])
        self.fx2 = int(fileCrystalBounds[1][0])
        self.fy2 = int(fileCrystalBounds[1][1])
        logger.debug("x1,x2,y1,y2, fx1, fy1 %d,%d,%d,%d,%d,%d" %
                     (x1,x2,y1,y2, self.fx1,self.fy1))
        pos = [x1-self.fx1,y1-self.fy1]
        roisize = [x2-x1, y2-y1]
        bounds = [0, 0, self.fx2-self.fx1, self.fy2-self.fy1]
        if self.roi is None:
            self.roi = RectROI(pos, roisize, movable=True, sideScalers=True, maxBounds=bounds)
            self.roi.addScaleHandle([0,.5], [1,.5])
            self.roi.addScaleHandle([.5,0], [.5,1])
            self.viewBox.addItem(self.roi, ignoreBounds=True)
        else:
            logger.debug("Setting position & size")
            self.roi.setSize(roisize,  update=False, finish=False)
            self.roi.setPos(pos, update=False, finish=False)
            logger.debug("Size %s" % self.roi.size())
            logger.debug("Position %s" % self.roi.pos())
            
            
        