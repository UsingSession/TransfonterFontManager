import os
import shutil
import re
from contextlib import redirect_stderr
from fontTools import ttLib
from commands.abstract_command import AbstractCommand

# https://gist.github.com/jorgegarciadev/6127832
class FontFaceCommand(AbstractCommand):

  def getProcessName():
    return 'Build @font-face'

  def process(items, contextConfig):
    cssFile = contextConfig.inputFontFaceFileName.text()
    isChecked = contextConfig.fontFaceGenerator.isChecked()
    os.chdir(contextConfig.directory)
    open(cssFile, '+w').write('')
    if isChecked:
      for dir_count, directory in enumerate(os.listdir(contextConfig.directory)):
        if(os.path.isdir(os.path.join(contextConfig.directory, directory))):
          items = list(os.listdir(os.path.join(contextConfig.directory, directory)))
          os.chdir(os.path.join(contextConfig.directory, directory))
          path = os.path.abspath(items[0])
          font =list( __class__.font_info(path))
          files_count = len(items)
          template =  "@font-face {"
          if not font[3]:
            template += "\n\tfont-family: '" + str(font[1]) + "';"
          else:
            template += "\n\tfont-family: '" + str(font[3]) + "';"
          template += "\n\tsrc:"
          for f_count, filename in enumerate(os.listdir(os.path.join(contextConfig.directory, directory))):
            names, file_extension = os.path.splitext(filename)
            file_extension = file_extension.replace('.', '')
            if(files_count == (f_count + 1)):
              template += "\n\t\turl('fonts/"  + directory + "/" + filename + "') format('"+file_extension+"');"
            else:
              template += "\n\t\turl('fonts/"  + directory + "/" + filename + "') format('"+file_extension+"'),"
          template += "\n\tfont-display: swap;"
          if(font[2] == 'Italic'):
            template += "\n\tfont-style: italic;"
          else:
            template += "\n\tfont-style: normal;"
            
          test_list = ['Thin',  'ExtraLight',
                      'Ultra Light', 'Light', 
                      'Normal', 'Book', 
                      'Regular', 'Medium', 
                      'SemiBold', 'DemiBold', 
                      'Bold', 'Extra Bold',
                      'Ultra Bold', 'Black',
                      'Heavy']
          weight = {
            'Thin' : 100 ,
            'ExtraLight' : 200 ,
            'Ultra Light' : 200 , 
            'Light' : 300, 
            'Normal': 400, 
            'Book': 400, 
            'Regular': 400, 
            'Medium': 500, 
            'SemiBold': 600, 
            'DemiBold': 600, 
            'Bold': 700, 
            'Extra Bold': 800,
            'Ultra Bold': 800, 
            'Black': 900,
            'Heavy': 900
          }
          
          for key, name in enumerate(test_list):
            res = font[0].find(name)
            if(res != -1):
              template += "\n\tfont-weight: "+ str(weight.get(name)) +";"
              break

          template += "\n}\n\n"
          os.chdir(contextConfig.directory)
          cssFile = os.path.abspath(cssFile)
          if os.path.exists(cssFile):
              append_write = 'a' # append if already exists
          else:
              append_write = '+w' # make a new file if not
          open(cssFile, append_write).writelines(template)

  def willDoProcess(item, contextConfig):
    return True

  def font_info(font_path):
      font = ttLib.TTFont(font_path, ignoreDecompileErrors=True)
      with redirect_stderr(None):
          names = font['name'].names

      details = {}
      for x in names:
          if x.langID == 0 or x.langID == 1033:
              try:
                  details[x.nameID] = x.toUnicode()
              except UnicodeDecodeError:
                  details[x.nameID] = x.string.decode(errors='ignore')

      return details[4], details[1], details[2], details.get(16)