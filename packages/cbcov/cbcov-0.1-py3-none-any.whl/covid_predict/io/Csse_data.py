import pandas as pd


class Csse_data():
    def __init__(self):
       self.url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
       self.files = ["time_series_covid19_confirmed_global.csv",
                     "time_series_covid19_deaths_global.csv",
                     "time_series_covid19_recovered_global.csv"]
       self.sep = ";"
       self.index_col = 2

    def save_csv():
        

    def _get_csv():
        return [pd.csv_read(self.url + self.file[i], parse_dates=True, sep=self.sep, index_col=2) for i in self.files_names]

    def get_type(type="deaths"):
        
    def get_country():

    def get_regions():


    
