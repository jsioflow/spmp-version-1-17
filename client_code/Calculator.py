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
    anvil.server.call('say_hello', 'Anvil Developer')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(f"The file's name is: {file.name}")
    print(f"The number of bytes in the file is: {file.length}")
    print(f"The file's content type is: {file.content_type}")
  #  print(f"The file's contents are: '{file.get_bytes()}'")
    self.label_2.text = file.name
    anvil.server.call('say_hello', 'Anvil Developer')
    self.rich_text_1.content = anvil.server.call('file_for_analysis',file)
   # if file.length > 125000:
   #   self.label_5.text = "File has 'Too Many Days' please refresh the page and resubmit"
   #   self.label_6.icon = "fa:refresh"
   #   self.label_6.icon_align = "left"
   #   self.label_6.foreground = "#e01010"
    pass