import datetime
import pandas as pd

period=""

def createDF(date1, date2):
    #formated in the input
    #setDate(date)
    #delta=setDelta(delta)
    #create the dataframe with the necesary years 
    df=getDataset(date1,date2)
    print("Se crea el dataframe")
    #put the colum "date" as the index
    df=dateToIndex(df)
    #group the df by datetime taking the mean of all the stations
    df=meanbyDate(df)
    print("Se formatea el dataframe")
    df=filterDFbyDate(df,date1,date2)
    return df

def setDate(date):
    #ToDo:validate format
    if len(date)>=10:
        day=int(date[8:10])
        setPeriod("D")
    else:
        day=1
        setPeriod("M")
    if len(date)>=7:
        month=int(date[5:7])
    else:
        month=1
        setPeriod("Y")
    year=int(date[:4])
    return datetime.date(year,month,day)
    
def setPeriod(periodChange):
    global period
    period=periodChange

def getPeriod():
    global period
    return period
    
    
def setDelta(delta):
    global period      
    if period=="M":
        return datetime.timedelta(days=delta*30)
    else:
        return datetime.timedelta(days=delta)


def getDataset(date1,date2):
    path="../Input/air-quality-madrid/csvs_per_year/madrid_{}.csv"
    #una fecha
    df_list=[]
    for year in range(date1.year,date2.year+1):
        df_list.append(pd.read_csv(path.format(year)))
    
    
    #dos fechas
    #if type(date2)==datetime.date and date2.year!=date1.year:
        
    
    
    #fecha y delta
    #elif type(date2)==datetime.timedelta:
    #    if (date1-date2).year!=date1.year:
    #        df_list.append(pd.read_csv(path.format((date1-date2).year)))
    #    if (date1+date2).year!=date1.year:
    #        df_list.append(pd.read_csv(path.format((date1+date2).year)))

    return pd.concat(df_list, axis=0, ignore_index=True,sort=False)


def dateToIndex(df):
    df["datetime"] = pd.to_datetime(df["date"])
    df = df.set_index('datetime')
    #df = df.drop(columns=["date"])
    return df


def meanbyDate(df):
    return df.groupby(['datetime']).mean()

def filterDFbyDate(df,date1,date2):
    filter_before=df.index.date>=(date1).date()
    filter_after=df.index.date<=(date2).date()

    return df[filter_before & filter_after]
