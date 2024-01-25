import anvil.files
from anvil.files import data_files
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from io import BytesIO
import pandas as pd
import numpy as np
import os
import time
import datetime as dt
from datetime import datetime, timedelta, date
from dateutil import parser
from anvil.google.drive import app_files

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
  print(f"Hello from the server, {name}")
  return [1, 2, 3, 4]
  
def PowerImportData(data):
    dfOriginalImport = data[data['Read Type'].str.contains("Import")]
    dfOriginalImport = dfOriginalImport.sort_values(by=['Read Date and End Time'], ascending=False)
    dfOriginalImport = dfOriginalImport.rename(columns={'Read Date and End Time':'Date'})
    dfOriginalImport['Date'] = pd.to_datetime(dfOriginalImport['Date'])
    dfOriginalImport = dfOriginalImport.reset_index()
    del dfOriginalImport['index']
    dfOriginalImport['Day'] = dfOriginalImport['Date'].dt.day_name()
    dfOriginalImport = dfOriginalImport[['Date','Day','MPRN','Meter Serial Number','Read Value','Read Type']]
    dfOriginalImport.set_index('Date', inplace=True)
    return (dfOriginalImport)
  
def PowerImportDataIncomplete(data):
    dfOriginalImport = data[data['Read Type'].str.contains("Import")]
    #dfOriginalImport = dfOriginalImport.rename(columns={'Read Date and End Time':'Date'})
    #dfOriginalImport['Date'] = pd.to_datetime(dfOriginalImport['Read Date and End Time'], format='mixed')
    dfOriginalImport['Date'] = pd.to_datetime(dfOriginalImport['Read Date and End Time'])
    dfOriginalImport['Day'] = dfOriginalImport['Date'].dt.day_name()
    #    for x in range(0,len(dfOriginalImport)):
    #        dfOriginalImport.loc[x,'Day'] = dfOriginalImport.loc[x,'Date'].day_name()
    dfOriginalImport = dfOriginalImport[['Date','Day','MPRN','Meter Serial Number','Read Value','Read Type']]
    print(dfOriginalImport.head(1))
    df1 = pd.DataFrame(columns=['Date','Count'])
    df2 = pd.DataFrame(columns=['Incomplete_Date','Count'])
    df1 = dfOriginalImport.groupby(dfOriginalImport['Date'].dt.date).size().reset_index(name='Count')
    for x in range (0, len(df1)):
        if df1.loc[x,'Count'] < 48:
            df2.loc[x,'Incomplete_Date'] = df1.loc[x,'Date']
            df2.loc[x,'Count'] = df1.loc[x,'Count']
    df2 = df2.reset_index(drop=True)
    
    dfOriginalImport['Filter_Date'] = dfOriginalImport['Date'].dt.date
    dfOriginalImport = dfOriginalImport.reset_index()
    
    for y in range (0, len(df2)):
        update_df = dfOriginalImport[dfOriginalImport.Filter_Date != df2.loc[y,'Incomplete_Date']]
        dfOriginalImport = update_df
    #print(dfOriginalImport.dtypes)
    
    dfOriginalImport = dfOriginalImport.reset_index()
    del dfOriginalImport['index']
    del dfOriginalImport['Filter_Date']
    return dfOriginalImport

def GenerateChargeMatrix(dfOriginalImport, dfTariffs, dfTariffs_days):
    dfChargeMatrix = dfOriginalImport
    dfChargeMatrix.reset_index(inplace=True)
    factor =0.5
    list1 = []
    list2 = []

    for x in range (0, len(dfChargeMatrix)-1):
        dfChargeMatrix.loc[x,'Total_Kwh'] = (dfChargeMatrix.loc[x,'Read Value'] * factor) + (dfChargeMatrix.loc[x+1,'Read Value'] * factor)
    dfChargeMatrix['Date'] = dfChargeMatrix['Date'].shift(-1)
    dfChargeMatrix = dfChargeMatrix.iloc[::2]
    dfChargeMatrix = dfChargeMatrix[['Date','Day','MPRN','Meter Serial Number','Read Type','Total_Kwh']]
    dfChargeMatrix = dfChargeMatrix.reset_index()
    del dfChargeMatrix['index']

    # Read list of Tariff options form file and populate the Charge Matrix
    for column in dfTariffs.columns:
        list1.append(column)
    del list1[0]
    for column in list1:
        dfChargeMatrix[column] = 0

    dfChargeMatrix['Hours'] = dfChargeMatrix.Date.dt.time
    for x in range (0, len(dfChargeMatrix)):
        dfChargeMatrix.loc[x,'Hours'] = str(dfChargeMatrix.loc[x,'Hours'])

    for l in range (len(list1)):
        tariffoption = (list1[l])
        for column in dfTariffs.columns:
            if column == tariffoption:
                for x in range (0, len(dfChargeMatrix)):
                    for y in range (0, len(dfTariffs)):
                        if dfChargeMatrix.loc[x,'Hours'] == dfTariffs.loc[y,'Hours']:
                            dfChargeMatrix.loc[x,tariffoption +'_Rate'] = dfTariffs.loc[y,tariffoption]

    for l in range (len(list1)):
        tariffoption = (list1[l])
        for column in dfTariffs_days.columns:
            if column == tariffoption:
                for x in range (0, len(dfChargeMatrix)):
                    for y in range (0, len(dfTariffs_days)):
                        if dfChargeMatrix.loc[x,'Day'] == dfTariffs_days.loc[y,'Day']:
                            dfChargeMatrix.loc[x,tariffoption +'_Y/N'] = dfTariffs_days.loc[y,tariffoption]
    dfChargeMatrix = dfChargeMatrix.drop(['Hours'], axis=1)

    dfSummary = pd.DataFrame(columns=['Tariff Plan','Total Cost'])

    for l in range (len(list1)):
        tariffoption = (list1[l])
        for x in range (0, len(dfChargeMatrix)):
            if dfChargeMatrix.loc[x,tariffoption+'_Y/N'] == 'Yes':
                dfChargeMatrix.loc[x,tariffoption] = round(((dfChargeMatrix.loc[x,'Total_Kwh'] * dfChargeMatrix.loc[x,tariffoption+'_Rate'])/100),4)
    
    # Day Count for Summary Statement
    daysevaluated = np.floor(x/24)

# Completing the calculations to derive the totals for each of the tariff options
    for l in range (len(list1)):
        tariffoption = (list1[l])
        dfSummary.loc[l,'Tariff Plan'] = tariffoption
        dfSummary.loc[l,'Total Cost'] = round((dfChargeMatrix[tariffoption].sum()),2)
    dfSummary = dfSummary.sort_values(['Total Cost'])
    for x in range(0, len(dfSummary)):
        dfSummary.loc[x,'Total Cost'] = '€'+str(dfSummary.loc[x,'Total Cost'])

    dfSummary.loc[x+2,'Tariff Plan'] = 'Total Number of days Evaluated'
    dfSummary.loc[x+2,'Total Cost'] = str(daysevaluated) + ' Days'

    dfSummary.reset_index(inplace=False)
    dfSummary = dfSummary.set_index('Tariff Plan')
    print(dfSummary)
    return dfSummary

@anvil.server.callable
def LoadOffshoreAssets(file):
  my_bytes=file.get_bytes()
  dfOriginal = pd.read_csv(BytesIO(my_bytes))
  if len(dfOriginal) > 2000:
    print('Error, Too Many Days Submitted')
  with open(data_files['Utility_Plans_Hours.csv']) as file1:
    dfTariffs = pd.read_csv(file1)
   # print(dfTariffs.head(1))
  with open(data_files['Utility_Plans_Days.csv']) as file2:
    dfTariffs_days = pd.read_csv(file2)
   # print(dfTariffs_days.head(1))
  #print(dfOriginal.head(1))
  
  #dfOriginalImport = PowerImportData(dfOriginal)
  dfOriginalImport = PowerImportDataIncomplete(dfOriginal)
  dfChargeMatrix = GenerateChargeMatrix(dfOriginalImport, dfTariffs, dfTariffs_days)
  #print('dfOriginal Sample Output',dfOriginalImport.head(1))
  #print('ChargeMatrix Output',dfChargeMatrix)
  #value = str(dfOriginal.loc[0,'MPRN'])
  return dfChargeMatrix.to_markdown()

#@anvil.server.callable
#def df_as_markdown():
#    with open(data_files['Utility_Plans_Days.csv']) as file2:
#      df = pd.read_csv(file2)
#    return df.to_markdown()
  
@anvil.server.callable
def return_text_from_file():
    # Read the contents of a file
    with open(data_files['Hello.txt']) as f:
        text = f.read()
    return text

@anvil.server.callable
def return_data_from_file():
  with open(data_files['Utility_Plans_Hours.csv']) as file1:
    dfHours = pd.read_csv(file1)
   # print(dfHours.head(1))
  with open(data_files['Utility_Plans_Days.csv']) as file2:
    dfDays = pd.read_csv(file2)
   # print(dfDays.head(1))


#  print(dfcustomerdata.head(1))
   #     data = dfhours.read()
   # file = 'Utility_Plans_Hours.csv'
   # my_bytes=file.get_bytes()
   # dfHours = pd.read_csv(BytesIO(my_bytes))
   # return dfHours
