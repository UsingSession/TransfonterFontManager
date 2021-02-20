class CollectionIterator:

  def __init__(self, items):
    self.items      = items
    self.itemsLen   = len(items)
    self.commands   = None
    self.callback   = None
    self.curentPos  = None
    self.mutationItem = None

  def map(self):
    for result in map(self.iteration, self.items):
      pass

  def iteration(self,item):
    for command in self.commands:
      mutationItem = command.process(item, self.contextConfig)
      index = self.items.index(item)
      self.items[index] = mutationItem
      item = mutationItem
      if self._callback != None:
        self._callback(command,mutationItem, self.items)
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