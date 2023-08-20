###------------------------------------------------------Coded By Reza Haghgoo------------------------------------------------------###
###------------------------------------------------------Last Edit : 6/10/2023------------------------------------------------------###
###---------------------------------------------Merging All Residential Consumption Data--------------------------------------------###

###-------------------------------------------------------Importing Libraries-------------------------------------------------------###

import pandas as pd
import numpy as np

###----------------------------------------------Importing Residential Consumption Data---------------------------------------------###

CD1 = pd.read_csv('CD1.csv')
CD2 = pd.read_csv('CD2.csv')
CD3 = pd.read_csv('CD3.csv')
CD4 = pd.read_csv('CD4.csv')
CD5 = pd.read_csv('CD5.csv')
CD6 = pd.read_csv('CD6.csv')

###----------------------------------------------------Seting ID column as Index----------------------------------------------------###

CD1 = CD1.set_index(CD1['ID'])
CD2 = CD2.set_index(CD2['ID'])
CD3 = CD3.set_index(CD3['ID'])
CD4 = CD4.set_index(CD4['ID'])
CD5 = CD5.set_index(CD5['ID'])
CD6 = CD6.set_index(CD6['ID'])

###-------------------------------------------------------Deleting ID column--------------------------------------------------------###

CD1.drop('ID', axis=1, inplace=True)
CD2.drop('ID', axis=1, inplace=True)
CD3.drop('ID', axis=1, inplace=True)
CD4.drop('ID', axis=1, inplace=True)
CD5.drop('ID', axis=1, inplace=True)
CD6.drop('ID', axis=1, inplace=True)

###---------------------------------------------Merging All Residential Consumption Data--------------------------------------------###

ResConsumptionData = pd.concat([CD1, CD2, CD3, CD4, CD5, CD6])

###-----------------------------------------Deleting the Columns with the Time more than 48-----------------------------------------###

DeleteColum1 = [29749 + i for i in range(0,47)]
DeleteColum2 = [29849 + i for i in range(0,47)]
DeleteColum3 = [29949 + i for i in range(0,47)]
DeleteColum4 = [30049 + i for i in range(0,47)]
DeleteColum5 = [30149 + i for i in range(0,47)]
DeleteColum6 = [30249 + i for i in range(0,47)]
DeleteColum7 = ['66949', '66950']

DeleteColum1 = list(map(str, DeleteColum1))
DeleteColum2 = list(map(str, DeleteColum2))
DeleteColum3 = list(map(str, DeleteColum3))
DeleteColum4 = list(map(str, DeleteColum4))
DeleteColum5 = list(map(str, DeleteColum5))
DeleteColum6 = list(map(str, DeleteColum6))

ResConsumptionData.drop(DeleteColum1, axis=1, inplace=True)
ResConsumptionData.drop(DeleteColum2, axis=1, inplace=True)
ResConsumptionData.drop(DeleteColum3, axis=1, inplace=True)
ResConsumptionData.drop(DeleteColum4, axis=1, inplace=True)
ResConsumptionData.drop(DeleteColum5, axis=1, inplace=True)
ResConsumptionData.drop(DeleteColum6, axis=1, inplace=True)
ResConsumptionData.drop(DeleteColum7, axis=1, inplace=True)

###------------------------------------------Adding the 45202 and 45203 Columns to Dataset------------------------------------------###

ResConsumptionData = ResConsumptionData.assign(**{'45202':[np.nan] * len(ResConsumptionData)})
ResConsumptionData = ResConsumptionData.assign(**{'45203':[np.nan] * len(ResConsumptionData)})

###-------------------------------------------------------Sorting Columns-----------------------------------------------------------###

ResConsumptionData.sort_index(axis=1, inplace=True)

###--------------------------------------------Exporting All Residential Consumption Data-------------------------------------------###

ResConsumptionData.to_csv('Consumption Data of All Residential Meters.csv')