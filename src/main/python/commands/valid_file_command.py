import os, shutil
from commands.abstract_command import AbstractCommand

class ValidFileCommand(AbstractCommand):

  def getProcessName():
    return 'Check file: '

  def process(item, contextConfig):
    return item
  
  def willDoProcess(item, contextConfig):
    avaible_extensions = ['.woff', '.woff2', '.ttf', '.svg']
    if not os.path.isdir(os.path.join(contextConfig.directory, item)):
      names, file_extension = os.path.splitext(item)
      if file_extension in avaible_extensions:
        return True
      else:
        return False
    return False