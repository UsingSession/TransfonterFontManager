import os
from commands.abstract_command import AbstractCommand

class RenameCommand(AbstractCommand):

  @staticmethod
  def getProcessName():
    return 'Renaming file: '

  @staticmethod
  def process(item, contextConfig):
    str_replace = contextConfig.input_substring.text()
    if str_replace:
      if not os.path.isdir(os.path.join(contextConfig.directory, item)):
        names, file_extension = os.path.splitext(item)
        dst = contextConfig.directory + '/' + names.replace(str_replace, '') + file_extension
        src = contextConfig.directory + '/' + names + file_extension
        os.rename(src, dst)
        return names.replace(str_replace, '') + file_extension
    return item

  def willDoProcess(item, contextConfig):
    return True