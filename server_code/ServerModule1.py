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

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
@anvil.server.callable
def build_pdf(data1, data2):
  pdf_file = anvil.pdf.render_form('Form1', data1, data2)
  return pdf_file
