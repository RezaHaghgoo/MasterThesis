###------------------------------------------------------Coded By Reza Haghgoo------------------------------------------------------###
###------------------------------------------------------Last Edit : 6/10/2023------------------------------------------------------###
###--------------------------------------------Filtering Residential Meters for each Part-------------------------------------------###

###-------------------------------------------------------Importing Libraries-------------------------------------------------------###

import pandas as pd

###----------------------------------------------------Importing Consumption Data---------------------------------------------------###

CD1_tb = pd.read_table('File1.txt')
CD2_tb = pd.read_table('File2.txt')
CD3_tb = pd.read_table('File3.txt')
CD4_tb = pd.read_table('File4.txt')
CD5_tb = pd.read_table('File5.txt')
CD6_tb = pd.read_table('File6.txt')

###--------------------------------------------------Importing Residential Meters ID------------------------------------------------###

ResMeters = pd.read_excel('Residential Meters.xlsx', sheet_name='Sheet1')

RM1 = ResMeters[0:651]
RM2 = ResMeters[651:1317]
RM3 = ResMeters[1317:1966]
RM4 = ResMeters[1966:2624]
RM5 = ResMeters[2624:3273]
RM6 = ResMeters[3273:4225]

###-------------------------------------------------Converting Tables into Dataframes-----------------------------------------------###

CD1 = pd.DataFrame(CD1_tb)
CD2 = pd.DataFrame(CD2_tb)
CD3 = pd.DataFrame(CD3_tb)
CD4 = pd.DataFrame(CD4_tb)
CD5 = pd.DataFrame(CD5_tb)
CD6 = pd.DataFrame(CD6_tb)

###-------------------------------------------------Spliting Columns of Consumption Data--------------------------------------------###

CD1[['ID','Time','Power']] = CD1.Data.str.split(" ",expand=True,)
CD2[['ID','Time','Power']] = CD2.Data.str.split(" ",expand=True,)
CD3[['ID','Time','Power']] = CD3.Data.str.split(" ",expand=True,)
CD4[['ID','Time','Power']] = CD4.Data.str.split(" ",expand=True,)
CD5[['ID','Time','Power']] = CD5.Data.str.split(" ",expand=True,)
CD6[['ID','Time','Power']] = CD6.Data.str.split(" ",expand=True,)

###-----------------------------------------------Deleting the first column that is merged------------------------------------------###

CD1.drop('Data', axis=1, inplace=True)
CD2.drop('Data', axis=1, inplace=True)
CD3.drop('Data', axis=1, inplace=True)
CD4.drop('Data', axis=1, inplace=True)
CD5.drop('Data', axis=1, inplace=True)
CD6.drop('Data', axis=1, inplace=True)

###---------------------------------------------------Reshaping the Consumption Table-----------------------------------------------###

CD1 = CD1.drop_duplicates(subset=['ID', 'Time'])
CD1Reshaped = CD1.pivot(index='ID', columns='Time', values='Power')

CD2 = CD2.drop_duplicates(subset=['ID', 'Time'])
CD2Reshaped = CD2.pivot(index='ID', columns='Time', values='Power')

CD3 = CD3.drop_duplicates(subset=['ID', 'Time'])
CD3Reshaped = CD3.pivot(index='ID', columns='Time', values='Power')

CD4 = CD4.drop_duplicates(subset=['ID', 'Time'])
CD4Reshaped = CD4.pivot(index='ID', columns='Time', values='Power')

CD5 = CD5.drop_duplicates(subset=['ID', 'Time'])
CD5Reshaped = CD5.pivot(index='ID', columns='Time', values='Power')

CD6 = CD6.drop_duplicates(subset=['ID', 'Time'])
CD6Reshaped = CD6.pivot(index='ID', columns='Time', values='Power')

###---------------------------------------------Converting Index Type From Text to Number-------------------------------------------###

CD1Reshaped.index = pd.to_numeric(CD1Reshaped.index)
CD2Reshaped.index = pd.to_numeric(CD2Reshaped.index)
CD3Reshaped.index = pd.to_numeric(CD3Reshaped.index)
CD4Reshaped.index = pd.to_numeric(CD4Reshaped.index)
CD5Reshaped.index = pd.to_numeric(CD5Reshaped.index)
CD6Reshaped.index = pd.to_numeric(CD6Reshaped.index)

###-------------------------------------------------Filtering only Residentual Meters-----------------------------------------------###

CD1 = CD1Reshaped.loc[RM1.loc[:,'Res Meters']]
CD2 = CD2Reshaped.loc[RM2.loc[:,'Res Meters']]
CD3 = CD3Reshaped.loc[RM3.loc[:,'Res Meters']]
CD4 = CD4Reshaped.loc[RM4.loc[:,'Res Meters']]
CD5 = CD5Reshaped.loc[RM5.loc[:,'Res Meters']]
CD6 = CD6Reshaped.loc[RM6.loc[:,'Res Meters']]

###---------------------------------------------Exporting Residentual Meters for each Part------------------------------------------###

CD1.to_csv('CD1.csv')
CD2.to_csv('CD2.csv')
CD3.to_csv('CD3.csv')
CD4.to_csv('CD4.csv')
CD5.to_csv('CD5.csv')
CD6.to_csv('CD6.csv')