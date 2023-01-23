
from meteo_downloader_noaa import meteo_downloader

station_list = ['26063099999', '26058099999']
years = [2010, 2023]
out_folder = 'F:/SCIENCE 2023/Climate Data/st.petersburg/'

meteo_downloader(station_list=station_list, years=years, out_folder=out_folder)


