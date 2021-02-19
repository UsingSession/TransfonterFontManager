from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from threading import Timer
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import pathlib, os, shutil, sys
from utility.collection_iterator import CollectionIterator

from commands.copy_command import CopyCommand

appctxt = ApplicationContext()
Form, _ = uic.loadUiType(appctxt.get_resource("app.ui"))

class TransfonterFontManager(QtWidgets.QMainWindow, Form):

  def __init__(self):
    super(TransfonterFontManager, self).__init__()
    # Isolation of a class for processing
    self.iterator = CollectionIterator
    self.setupUi(self)
    self.init_UI()
    self.directory = '~/'

  def openDirectory(self, e):
    self.directory = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)

  def clearProgress(self):
    self.progressBar.setValue(0)
    self.centralwidget.setEnabled(True)
    
  def run(self, e):
    self.textEdit.setText('')
    self.iterator(os.listdir(self.directory)).setCommands([
      CopyCommand
    ]).setAlter(self.viewAlter).map()
    
    self.renameFiles()
    self.groupFiles()
    self.progressBar.setValue(100)
    self.centralwidget.setDisabled(True)
    Timer(2.0, self.clearProgress).start()

  def renameFiles(self):
    str_replace = self.input_substring.text()
    if str_replace:
      for count, filename in enumerate(os.listdir(self.directory)):
        if not os.path.isdir(os.path.join(self.directory, filename)):
          names, file_extension = os.path.splitext(filename)
          dst = self.directory + '/' + names.replace(str_replace, '') + file_extension
          src = self.directory + '/' + names + file_extension
          os.rename(src, dst)
  
  def groupFiles(self):
    if self.checkBox.isChecked():
      for count, filename in enumerate(os.listdir(self.directory)):
        if not os.path.isdir(os.path.join(self.directory, filename)):
            names, file_extension = os.path.splitext(filename)
            dst = self.directory + '/' + names + file_extension
            path = self.directory + '/' + names
            if not os.path.isdir(path):
              os.mkdir(path)
            shutil.move(dst, path + '/' + names + file_extension)

  def viewAlter(self, command, mutationItem, items):
    self.progressBar.setValue(round((items.index(mutationItem) * 100) / len(items)))
    isNewLine = '\n' if self.textEdit.toPlainText() else ''
    self.textEdit.setText(self.textEdit.toPlainText() + isNewLine + command.getProcessName() + ' ' + str(mutationItem))

  def getIcon(self, name):
    return QIcon(appctxt.get_resource(name))

  def init_UI(self):
    self.setWindowIcon(self.getIcon("favicon.png"))
    self.directory_button.setIcon(self.getIcon("folder.png"))
    self.directory_button.clicked.connect(self.openDirectory)
    self.run_button.clicked.connect(self.run)
    self.textEdit.setReadOnly(True)

if __name__ == '__main__':
  window = TransfonterFontManager()
  window.show()
  exit_code = appctxt.app.exec_()
  sys.exit(exit_code)