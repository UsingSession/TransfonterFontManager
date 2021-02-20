import os, shutil

class GroupCommand():

  @staticmethod
  def getProcessName():
    return 'Moving file: '

  @staticmethod
  def process(item, contextConfig):
    name = item
    if contextConfig.checkBox.isChecked():
      if not os.path.isdir(os.path.join(contextConfig.directory, item)):
          names, file_extension = os.path.splitext(item)
          dst = contextConfig.directory + '/' + names + file_extension
          path = contextConfig.directory + '/' + names
          if not os.path.isdir(path):
            os.mkdir(path)
          shutil.move(dst, path + '/' + names + file_extension)
          name = names + file_extension
    return name