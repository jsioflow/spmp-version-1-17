from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.rich_text_1.content = Globals.answer
    self.rich_text_2.content = Globals.recommendation
    # Any code you write here will run before the form opens.

  def rich_text_1_show(self, **event_args):
    """This method is called when the RichText is shown on the screen"""
    #self.rich_text_1.content = answer
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    #self.rich_text_1.content = answer
    pass
