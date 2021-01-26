from PyQt5 import uic, QtWidgets
import pathlib, os, shutil
from PyQt5 import QtCore, QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon

Form, _ = uic.loadUiType(str(pathlib.Path(__file__).parent.absolute()) + '/ui/' + "app.ui")

class TransfonterFontManager(QtWidgets.QMainWindow, Form):
  
  def __init__(self):
    super(TransfonterFontManager, self).__init__()
    self.setupUi(self)
    self.init_UI()
    self.directory = '~/'

  def openDirectory(self, e):
    self.directory = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)

  def run(self, e):
    str_replace = self.input_substring.text()
    if str_replace:
      for count, filename in enumerate(os.listdir(self.directory)):
        if not os.path.isdir(os.path.join(self.directory, filename)):
          names, file_extension = os.path.splitext(filename)
          dst = self.directory + '/' + names.replace(str_replace, '') + file_extension
          src = self.directory + '/' + names + file_extension
          os.rename(src, dst)
          if self.checkBox.isChecked():
            path = self.directory + '/' + names.replace(str_replace, '')
            if not os.path.isdir(path):
              os.mkdir(path)
            shutil.move(dst, path + '/' + names.replace(str_replace, '') + file_extension)
    elif self.checkBox.isChecked():
      for count, filename in enumerate(os.listdir(self.directory)):
        if not os.path.isdir(os.path.join(self.directory, filename)):
          names, file_extension = os.path.splitext(filename)
          dst = self.directory + '/' + names.replace(str_replace, '') + file_extension
          if self.checkBox.isChecked():
            path = self.directory + '/' + names.replace(str_replace, '')
            if not os.path.isdir(path):
              os.mkdir(path)
            shutil.move(dst, path + '/' + names.replace(str_replace, '') + file_extension)

  def init_UI(self):
    self.setWindowTitle('File Manager for file')
    self.input_substring.setPlaceholderText('Enter the input string.')
    self.directory_button.setIcon(QIcon(str(pathlib.Path(__file__).parent.absolute()) + '/static/img/' + 'folder.png')) 
    self.directory_button.clicked.connect(self.openDirectory)
    self.run_button.clicked.connect(self.run)


if __name__ == '__main__':
  import sys
  app = QtWidgets.QApplication(sys.argv)
  window = TransfonterFontManager()
  window.show()
  sys.exit(app.exec_())