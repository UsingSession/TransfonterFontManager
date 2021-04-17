import os, sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from threading import Timer
from fbs_runtime.application_context.PyQt5 import ApplicationContext
# Project scripts
from utility.collection_iterator import CollectionIterator
from commands.valid_file_command import ValidFileCommand
from commands.rename_command import RenameCommand
from commands.group_command import GroupCommand

appctxt = ApplicationContext()
Form, _ = uic.loadUiType(appctxt.get_resource("app.ui"))

class TransfonterFontManager(QtWidgets.QMainWindow, Form):

  def __init__(self):
    super(TransfonterFontManager, self).__init__()
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
    self.processMessage.setText('')
    self.iterator(os.listdir(self.directory)).setCommands([
      ValidFileCommand,
      RenameCommand,
      GroupCommand,
    ]).setContextConfig(self).setAlter(self.viewAlter).map()

    self.progressBar.setValue(100)
    self.centralwidget.setDisabled(True)
    Timer(1.3, self.clearProgress).start()

  def viewAlter(self, command,mutationItem, items):
    self.progressBar.setValue(round((items.index(mutationItem) * 100) / len(items)))
    isNewLine = '\n' if self.processMessage.toPlainText() else ''
    self.processMessage.setText(self.processMessage.toPlainText() + isNewLine + '-> ' +  command.getProcessName() + ' ' + str(mutationItem))

  def getIcon(self, name):
    return QIcon(appctxt.get_resource(name))

  def init_UI(self):
    self.setWindowIcon(self.getIcon("favicon.png"))
    self.directory_button.setIcon(self.getIcon("folder.png"))
    self.directory_button.clicked.connect(self.openDirectory)
    self.run_button.clicked.connect(self.run)
    self.fontFaceGenerator.stateChanged.connect(self.collapse_input)
    self.processMessage.setReadOnly(True)

  def collapse_input(self):
    ffName    = self.inputFontFaceFileName
    isChecked = self.fontFaceGenerator.isChecked()
    ffName.setHidden(not isChecked)

if __name__ == '__main__':
  window = TransfonterFontManager()
  window.show()
  exit_code = appctxt.app.exec_()
  sys.exit(exit_code)