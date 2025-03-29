import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
#вижет
app = QApplication([])
win = QWidget()



win.resize(800,400)
win.setWindowTitle("Лёгкий редакторр")
btn_dir = QPushButton("Папкка")
lw_files = QListWidget()
lb_image = QLabel("Картинка")

btn_left = QPushButton("← Anticlockwise ←")
btn_right = QPushButton("→ Clockwise →")
btn_flip = QPushButton("← Mirror →")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("Black/White")
btn_save = QPushButton("Save")
btn_save.setStyleSheet("background-color: #00aa00; color:#ffffff;")
btn_reset = QPushButton("Reset")
btn_reset.setStyleSheet("background-color: #aa0000; color:#ffffff;")

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_save)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_reset)
row_tools.addWidget(btn_right)
col2.addLayout(row_tools)

row.addLayout(col1,20)
row.addLayout(col2,80)
win.setLayout(row)

win.show()

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def showFilenamesList():
    extensions = [".jpg",".jpeg",".png",".gif",".bmp", ".PNG"]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.reseted = True
        self.save_dir = "Modified/"
    
    def loadImage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)
        self.reseted = True
        print(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        print(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        print(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        print(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        print(image_path)
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        print(image_path)
    def saveImage(self):
        path = os.path.join(self.dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        print(image_path)
    def resetImage(self):
        image_path = os.path.join(workdir, self.dir, self.filename)
        self.showImage(image_path)
        self.reseted = True
        print(image_path)
    def showImage(self,path):
        pixmapimage = QPixmap(path)
        label_width,label_height=lb_image.width(),lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width,label_height,Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)
workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_reset.clicked.connect(workimage.resetImage)
btn_right.clicked.connect(workimage.do_right)
btn_left.clicked.connect(workimage.do_left)
btn_sharp.clicked.connect(workimage.do_sharp)












app.exec_()
#лайаут