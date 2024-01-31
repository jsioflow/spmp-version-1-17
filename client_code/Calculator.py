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
    anvil.users.login_with_form()
    print(f"This user has logged in: {anvil.users.get_user()['email']}")

 # Any code you write here will run when the form opens.
    anvil.server.call('say_hello', 'Anvil Developer')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(f"The file's name is: {file.name}")
    print(f"The number of bytes in the file is: {file.length}")
    print(f"The file's content type is: {file.content_type}")
  #  print(f"The file's contents are: '{file.get_bytes()}'")
    self.label_2.text = file.name
    folder1 = app_files.uploads
    new_file = folder1.create_file(file.name)
    new_file.set_media(self.file_loader_1.file)
    anvil.server.call('say_hello', 'Anvil Developer')
    self.rich_text_1.content = anvil.server.call('file_for_analysis',file)

  pass