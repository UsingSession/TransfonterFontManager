

class CollectionIterator:

  def __init__(self, items):
    super(CollectionIterator, self).__init__()
    self.items = items
    self.callback = None

  def setCommands(self, commands):
    self.commands = commands
    return self

  def getCommands(self):
    return self.commands

  def withAlter(self, callback):
    self._callback = callback
    return self

  def map(self):
    for result in map(self.iteration, self.items):
      pass

  def iteration(self,item):
    for command in self.commands:
      mutationItem = command.process(item)
      if self._callback != None:
        self._callback(command, mutationItem)
      return mutationItem
