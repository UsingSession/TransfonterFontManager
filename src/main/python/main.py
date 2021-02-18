from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from threading import Timer
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import pathlib, os, shutil, sys
from utility.collection_iterator import CollectionIterator

from utility.copy import Copy

appctxt = ApplicationContext()
Form, _ = uic.loadUiType(appctxt.get_resource("app.ui"))

class TransfonterFontManager(QtWidgets.QMainWindow, Form):

  def __init__(self):
    super(TransfonterFontManager, self).__init__()

    # Isolation of a class for processing
    iterator = CollectionIterator([1,2,3, 9])
    iterator.setCommands([Copy]).withAlter(self.alter).map()

    self.setupUi(self)
    self.init_UI()
    self.directory = '~/'

  def alter(self, command, item):
    print(item)

  def openDirectory(self, e):
    self.directory = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)

  def clearProgress(self):
    self.progressBar.setValue(0)
    self.centralwidget.setEnabled(True)
    
  def run(self, e):
    
    self.countFiles = len(os.listdir(self.directory))
    self.renameFiles()
    self.groupFiles()
    self.progressBar.setValue(100)
    self.centralwidget.setDisabled(True)
    Timer(2.0, self.clearProgress).start()

  def renameFiles(self):
    str_replace = self.input_substring.text()
    if str_replace:
      for count, filename in enumerate(os.listdir(self.directory)):
        self.progressBar.setValue(round((count * 100) / self.countFiles))
        if not os.path.isdir(os.path.join(self.directory, filename)):
          names, file_extension = os.path.splitext(filename)
          dst = self.directory + '/' + names.replace(str_replace, '') + file_extension
          src = self.directory + '/' + names + file_extension
          os.rename(src, dst)
  
  def groupFiles(self):
    if self.checkBox.isChecked():
      for count, filename in enumerate(os.listdir(self.directory)):
        self.progressBar.setValue(round((count * 100) / self.countFiles))
        if not os.path.isdir(os.path.join(self.directory, filename)):
            names, file_extension = os.path.splitext(filename)
            dst = self.directory + '/' + names + file_extension
            path = self.directory + '/' + names
            if not os.path.isdir(path):
              os.mkdir(path)
            shutil.move(dst, path + '/' + names + file_extension)

  def init_UI(self):
    self.setWindowIcon(QIcon(appctxt.get_resource("favicon.png")))
    self.directory_button.setIcon(QIcon(appctxt.get_resource("folder.png")))
    self.directory_button.clicked.connect(self.openDirectory)
    self.run_button.clicked.connect(self.run)

if __name__ == '__main__':
  window = TransfonterFontManager()
  window.show()
  exit_code = appctxt.app.exec_()
  sys.exit(exit_code)