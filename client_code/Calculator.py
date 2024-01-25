from ._anvil_designer import CalculatorTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import time
import json
import anvil.http
from time import sleep
import anvil.media
from anvil.google.drive import app_files

class Calculator(CalculatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  # Any code you write here will run when the form opens.
    # Download this file from the default folder in Google Drive
   # file = app_files.utility_plans_days_csv
   # anvil.media.download(file)
   # testdf = file.get_bytes()
   # print(testdf)
   # print(file.get_bytes())

    # Hello Test from Server Function
   # return_value = anvil.server.call('say_hello', 'Anvil Developer')
   # print(f"The return value was {return_value}")

  # Any code you write here will run when the form opens.
    anvil.server.call('say_hello', 'Anvil Developer')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(f"The file's name is: {file.name}")
    print(f"The number of bytes in the file is: {file.length}")
    print(f"The file's content type is: {file.content_type}")
  #  print(f"The file's contents are: '{file.get_bytes()}'")
    self.label_2.text = file.name
    if file.length > 125000:
      self.label_5.text = "File has 'Too Many Days' please refresh the page and resubmit"
      self.label_6.icon = "fa:refresh"
      self.label_6.icon_align = "left"
      self.label_6.foreground = "#e01010"
    
   # folder1 = app_files.uploads
   # new_file = folder1.create_file(file.name)
   # new_file.set_media(self.file_loader_1.file)
    anvil.server.call('file_for_analysis',file)

    #folder2 = app_files.uploads_archive
    #new_file = folder2.create_file(file.name)
    #new_file.set_media(self.file_loader_1.file)
    pass

    # Test dataframe import from CSV in Google within Server Function
    self.rich_text_1.content = anvil.server.call('LoadOffshoreAssets', new_file)
    #print('MPRN Value Returned from Server',customerMPRN)
    #print('\r\n')

    # client side
    #self.rich_text_1.content = anvil.server.call('df_as_markdown')
    
    #filecontents = anvil.server.call('return_data_from_file')
    #print('File Contents from Server',filecontents)
    
    # List the files in the uploads folder
    #folder = app_files.uploads
    #for f in folder.list_files():
   #   print(f["title"])

    # Any code you write here will run when the form opens.