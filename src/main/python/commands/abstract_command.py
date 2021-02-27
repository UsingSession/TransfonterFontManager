class AbstractCommand():

    def getProcessName():
      raise NotImplementedError('subclasses must override getProcessName()!')

    def willDoProcess(item, contextConfig):
      raise NotImplementedError('subclasses must override isValidOperation()!')

    def process(item, contextConfig):
      raise NotImplementedError('subclasses must override process()!')