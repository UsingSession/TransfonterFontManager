from commands.abstract_command import AbstractCommand
from PyQt5.QtWidgets import QMessageBox

class CollectionIterator:

  def __init__(self, items):
    self.items        = items
    self.itemsLen     = len(items)
    self.commands     = None
    self.callback     = None
    self.curentPos    = None
    self.mutationItem = None

  def map(self):
    for result in map(self.iteration, self.items):
      pass
    return self

  def end(self, callback ):
    callback(self.items)

  def iteration(self,item):
    for command in self.commands:
      if self.isValidCommand(command):
        doProcess = command.willDoProcess(item, self.contextConfig)
        if not doProcess:
          return item
        else:
          mutationItem = command.process(item, self.contextConfig)
          index = self.items.index(item)
          self.items[index] = mutationItem
          item = mutationItem
          if self._callback != None:
            self._callback(command,mutationItem, self.items)
      else:
        self.getInvalidMessage(command)
        self.commands.remove(command)
    return item

  def getCommands(self):
    return self.commands

  def setContextConfig(self, contextConfig):
    self.contextConfig = contextConfig
    return self

  def setCommands(self, commands):    
    self.commands = commands
    return self

  def setAlter(self, callback):
    self._callback = callback
    return self

  def isValidCommand(self, command):
    return issubclass(command, AbstractCommand)

  def getInvalidMessage(self, command):
    message = "%s is not extends %s" % (str(command.__name__), str(AbstractCommand.__name__))
    QMessageBox.about(self.contextConfig, "Commands extends error", message)
