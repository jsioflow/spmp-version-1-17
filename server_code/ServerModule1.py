import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
import anvil.media
from . import Globals
from . Form1 import Form1

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
testvariable = Globals.testvariable
answer = Globals.answer
recommendation = Globals.recommendation

@anvil.server.callable
def build_pdf():
  print('This is a test',answer)
  pdf_file = anvil.pdf.render_form('Form1', recommendation, answer)
  anvil.media.write_to_file(pdf_file, 'test_pdf')
  return pdf_file
