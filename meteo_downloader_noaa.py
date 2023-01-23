import os
import urllib.request
import pandas as pd
from meteo_noaa_parser import meteo_parser

def meteo_downloader(data_period='hour',
                     out_folder=os.getcwd()+'/',
                     station_list=[],
                     years=[]):
    '''
    data_period - measurement period for downloaded data ("hour", "day"); default = "hour";

    station_list - list of required WMO stations; see the station list in the "station_list.txt" file
    (USAF + WBAN columns without space), for example "26063699999" for ST. PETERSBURG station;

    years - list of the required years; see observation boundaries for stations in the
    "station_list.txt" file (columns: BEGIN and END);

    out_folder - folder to save data; default = './noaa_data/

    function return data_frame with download error exceptions for each station
    '''

    # URL NOAA CLIMATE DATABASE DEFINITION
    if data_period == 'day':
        url_noaa = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/'  # daily data
    elif data_period == 'hour':
        url_noaa = 'https://www.ncei.noaa.gov/data/global-hourly/access/'  # hourly data
    else:
        raise ValueError('data_period name must be "hour" (hourly data) or "day" (daily data)')

    #CREATE YEARS RANGE
    years = range(years[0], years[1]+1)

    #CREATE FOLDERS FOR YEARS
    for year in years:
        try:
            folder_name = out_folder+str(year)
            os.mkdir(folder_name)
        except:
            pass

    #CREATE EXCEPTION DICT
    exceptions = []

    #DOWNLOAD DAILY METEO DATA FOR YEARS
    for year in years:
        for name in station_list:
            try:
                url = url_noaa+str(year)+'/'+name+'.csv'
                out = out_folder+str(year)+'/'+name+'.csv'
                out_parsed = out_folder + str(year) + '/' + name + '_parsed.csv'
                urllib.request.urlretrieve(url, out)
                meteo_parser(csv_file=out, out_file=out_parsed)

            except Exception as e:
                exceptions.append([name, year, e])


    #EXPORT EXCEPTIONS INTO CSV
    df_exceptions = pd.DataFrame(exceptions, columns=['ID', 'Year', 'Error'])



    return df_exceptions
