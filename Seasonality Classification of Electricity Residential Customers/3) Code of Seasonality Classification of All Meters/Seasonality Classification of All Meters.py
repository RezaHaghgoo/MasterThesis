###------------------------------------------------------Coded By Reza Haghgoo------------------------------------------------------###
###------------------------------------------------------Last Edit : 8/12/2023------------------------------------------------------###
###----------------------------------------------Seasonality Classification of All Meters-------------------------------------------###

###-------------------------------------------------------Importing Libraries-------------------------------------------------------###

import pandas as pd

###----------------------------------------------Importing Residential Consumption Data---------------------------------------------###

ResConsumptionData = pd.read_csv('Consumption Data of All Residential Meters.csv')

"""---------------------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------Preprocessing of Dataset-----------------------------------------------------"""
"""---------------------------------------------------------------------------------------------------------------------------------"""

###-----------------------------------------------------Primary Edit of Dataset-----------------------------------------------------###

ResConsumptionData = ResConsumptionData.set_index(ResConsumptionData['ID'])
ResConsumptionData.drop('ID', axis=1, inplace=True)
ResConsumptionDataT = ResConsumptionData.transpose()

###-------------------------------------------------------Indexing to Dataset-------------------------------------------------------###

Dateindex = pd.date_range(start='2009-01-01 00:29:59', end='2010-06-20 23:59:59', freq='30min')
ResConsumptionDataT = ResConsumptionDataT.set_index(Dateindex)
RCD_Day = ResConsumptionDataT.resample('D').sum()
indx_Date = RCD_Day.index
indx_Date = indx_Date.astype(str)
RCD_WeekDay = RCD_Day.copy()
indx1 = RCD_WeekDay.index
RCD_WeekDay.index = indx1.strftime('%A')
indx_WeekDay = RCD_WeekDay.index
RCD_WeekNumber = RCD_Day.copy()
indx2 = RCD_WeekNumber.index
RCD_WeekNumber.index = indx2.strftime('%U')
indx_WeekNumber = RCD_WeekNumber.index
indx_WeekNumber = pd.to_numeric(indx_WeekNumber)
RCD_Year = RCD_Day.copy()
indx3 = RCD_Year.index
RCD_Year.index = indx3.strftime('%Y')
indx_Year = RCD_Year.index
indx_Year = pd.to_numeric(indx_Year)

indx_Date = pd.DataFrame(indx_Date)
indx_Year = pd.DataFrame(indx_Year)
indx_WeekNumber = pd.DataFrame(indx_WeekNumber)
indx_WeekDay = pd.DataFrame(indx_WeekDay)

Load = RCD_Day.copy()
Load['Date'] = indx_Date.values
Load['Year'] = indx_Year.values
Load['NumberWeeks'] = indx_WeekNumber.values
Load['WeekDay'] = indx_WeekDay.values

Load = Load.set_index([Load['Date'], Load['Year'], Load['NumberWeeks'], Load['WeekDay']])
Load.drop(['Date', 'Year', 'NumberWeeks', 'WeekDay'], axis=1, inplace=True)

"""---------------------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------Classification of Dataset-----------------------------------------------------"""
"""---------------------------------------------------------------------------------------------------------------------------------"""

###----------------------------------------Calculating Mean Value of Each Week for Each Meter---------------------------------------###

WeekMean = pd.DataFrame(columns = Load.columns)
WeekMean['Year'] = []           
WeekMean['Weeknumber'] = []
for id in Load.columns:
    i = 0
    for year in range(2009,2011):
        for weeknumber in range(0,53):
            WeekMean.loc[i,id] = Load.loc[:,year,weeknumber,:][[id]].mean().values[0]
            if id == Load.columns[0]:    
                WeekMean.loc[i,'Year'] = year
                WeekMean.loc[i,'Weeknumber'] = weeknumber
            i+=1

WeekMean = WeekMean.set_index([WeekMean['Year'], WeekMean['Weeknumber']])
WeekMean = WeekMean.drop('Year', axis=1)
WeekMean = WeekMean.drop('Weeknumber', axis=1)

###---------------------------Comparison Between Mean Value and Week Day Values of Each Week for Each Meter-------------------------###

MeterID = Load.columns
WeekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
Col = pd.MultiIndex.from_product([MeterID, WeekDays], names=["Meter ID", "Week Days"])
SeasonalDay = pd.DataFrame(columns = Col)
SeasonalDay['Year'] = []           
SeasonalDay['Weeknumber'] = []
for id in Load.columns:
    for WD in WeekDays:
        i=0
        for Year in range(2009,2011):
            for Weeknumber in range(0,53):
                SeasonalDay.loc[i,(id,WD)] = 1 if Load.loc[:,Year,Weeknumber,WD][[id]].values > WeekMean.loc[Year,Weeknumber][[id]].values else 0
                if id == Load.columns[0] and WD == WeekDays[0]:    
                    SeasonalDay.loc[i,'Year'] = Year
                    SeasonalDay.loc[i,'Weeknumber'] = Weeknumber
                i+=1

SeasonalDay = SeasonalDay.set_index([SeasonalDay['Year'], SeasonalDay['Weeknumber']])
SeasonalDay = SeasonalDay.drop('Year', axis=1)
SeasonalDay = SeasonalDay.drop('Weeknumber', axis=1)

###--------------------------------------------Deleting Rows That Are Out of Dataset's Range----------------------------------------###

for i in range(0,27):
    SeasonalDay.drop((2010,26 + i), inplace=True)

###--------------------------------------Calculating Continuity of Seasonality of Seasonal Meters-----------------------------------###

SeasonalDaySum = SeasonalDay.sum()
SeasonalDaySum = pd.DataFrame(SeasonalDaySum)
SeasonalDaySum = SeasonalDaySum.transpose()

###--------Comparison Continuity of Seasonality of Seasonal Meters Values with Continusity Factor and Creating Output Tables--------###

ContinusityFactor = 0.8
STable = pd.DataFrame(columns = WeekDays)
USTable = pd.DataFrame(columns = ['UnSeasonal Meters'])
for id in Load.columns:
    if SeasonalDaySum.loc[:,(id,'Sunday')].values > ContinusityFactor*SeasonalDay.shape[0] or SeasonalDaySum.loc[:,(id,'Monday')].values > ContinusityFactor*SeasonalDay.shape[0] or SeasonalDaySum.loc[:,(id,'Tuesday')].values > ContinusityFactor*SeasonalDay.shape[0] or SeasonalDaySum.loc[:,(id,'Wednesday')].values > ContinusityFactor*SeasonalDay.shape[0] or SeasonalDaySum.loc[:,(id,'Thursday')].values > ContinusityFactor*SeasonalDay.shape[0] or SeasonalDaySum.loc[:,(id,'Friday')].values > ContinusityFactor*SeasonalDay.shape[0] or SeasonalDaySum.loc[:,(id,'Saturday')].values > ContinusityFactor*SeasonalDay.shape[0]:
        for Day in ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']:
            if SeasonalDaySum.loc[:,(id,Day)].values > ContinusityFactor*SeasonalDay.shape[0]:
                STable.loc[id,Day] = 'Seasonal'
            else:
                STable.loc[id,Day] = 'UnSeasonal'   
    else:
        USTable.loc[id,'UnSeasonal Meters'] = 'UnSeasonal'

"""---------------------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------Exporting Outputs of Classification-------------------------------------------------"""
"""---------------------------------------------------------------------------------------------------------------------------------"""

###------------------------------------------------------Exporting Outputs----------------------------------------------------------###

STable.to_csv('List of Seasonal Meters.csv')
USTable.to_csv('List of UnSeasonal Meters.csv')