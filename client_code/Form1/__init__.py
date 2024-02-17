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
  def __init__(self, content, content1, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.rich_text_1.content = Globals.answer
    self.rich_text_2.content = Globals.recommendation
    self.rich_text_2.foreground = "#16d02b"
    content = Globals.answer
    content1 = Globals.recommendation
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    content = Globals.answer
    content1 = Globals.recommendation
    pdf_file = anvil.server.call('build_pdf', content, content1)
    anvil.media.download(pdf_file)
    pass