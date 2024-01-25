from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil_extras.utils import timed

#from ..Form1 import Form1
#from ..Form2 import Form2
#from ..Form3 import Form3
#from ..Form4 import Form4
from ..Form5 import Form5

class MainForm(MainFormTemplate):
  @timed
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #anvil.users.login_with_form()
    #print(f"This user has logged in: {anvil.users.get_user()['email']}")
  
    # Any code you write here will run when the form opens.
    #anvil.server.call('say_hello', 'Anvil Developer')
  
  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form5())
    pass
 
'''   
    
    parameter21 = anvil.server.call('get_parameter21')
    self.label_5.text = parameter21
    self.label_5.tooltip = "€ saved in terms of Standard Day Time Utility Rates"
    
    parameter22 = anvil.server.call('get_parameter22')
    kWh = "{:.2f}".format(float(parameter22))
    self.label_7.text = str(kWh) + ' kWh'
    self.label_7.tooltip = "kWh Generated from the Sun"
    
    Co2 = "{:.2f}".format((int(parameter22) * 468)/1000)
    self.label_10.text = str(Co2) + ' Kg Co2'
    self.label_10.tooltip = "468 gCO2/kWh for Ireland"
    
    parameter23 = anvil.server.call('get_parameter23')
    SP_Projection = "{:.2f}".format(float(parameter23))
    self.label_12.text = str(SP_Projection) + ' kWh'
    self.label_12.tooltip = "Solar Power Projection in kWh"
    
    get_todays_data = anvil.server.call('get_report5_data')
    
    Daily_Home_kWh = "{:.2f}".format(get_todays_data['Home_kWh'])
    Daily_SP_kWh = "{:.2f}".format(get_todays_data['SP_kWh'])
    Sell_Grid_kWh = "{:.2f}".format(get_todays_data['Grid_Sell'])
    Buy_Grid_kWh = "{:.2f}".format(get_todays_data['Grid_Buy'])
    
    if get_todays_data['Grid_Sell'] == 0:
      SelfConsumption = 0
      self.label_14.text = str(SelfConsumption) + '%'
    elif get_todays_data['SP_kWh'] == 0:
      SelfConsumption = 0
      self.label_14.text = str(SelfConsumption) + '%'
    else:
      SelfConsumption = (1 - (get_todays_data['Grid_Sell']/get_todays_data['SP_kWh']))*100
      SelfConsumption = "{:.2f}".format(SelfConsumption)
      self.label_14.text = str(SelfConsumption) + '%'
    
    Independence = (1 - (get_todays_data['Grid_Buy']/get_todays_data['Home_kWh']))*100
    if Independence < 0:
      Independence = 0
    Independence = "{:.2f}".format(Independence)
    self.label_16.text = str(Independence) + '%'

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form1())
    pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form2())
    pass
  
  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form3())
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("MainForm")
    pass

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form4())
    pass
    
  def form_refreshing_data_bindings(self, **event_args):
    """This method is called when refreshing_data_bindings is called"""
    pass
'''    
    

 











