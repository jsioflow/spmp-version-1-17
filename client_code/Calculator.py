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

class Calculator(CalculatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

 # Any code you write here will run when the form opens.
    anvil.users.login_with_form()
    print(f"This user has logged in: {anvil.users.get_user()['email']}")
    #anvil.server.call('say_hello', 'Anvil Developer')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_5.visible = True
    sleep(3)
    anvil.users.logout()
    anvil.users.login_with_form()
    ## Return to Main Screen if the User logs in again
    open_form("Calculator")
    pass

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(f"The file's name is: {file.name}")
    print(f"The number of bytes in the file is: {file.length}")
    print(f"The file's content type is: {file.content_type}")
  #  print(f"The file's contents are: '{file.get_bytes()}'")
    self.label_6.visible = True
    if file.content_type != 'text/csv':
      self.label_6.foreground = "#d01616"
      self.label_6.text = 'This is an invalid file, Please try again'
    if file.content_type == 'text/csv':
      self.label_6.foreground = "#16d02b"
      self.label_6.text = 'This is a valid file, Processing ....'
    self.label_2.text = file.name
    folder1 = app_files.uploads
    new_file = folder1.create_file(file.name)
    new_file.set_media(self.file_loader_1.file)
      #self.label_6.text = anvil.server.call('file_for_checking', file)
    self.rich_text_1.content = anvil.server.call('file_for_analysis',file)
    self.label_6.visible = False
  pass