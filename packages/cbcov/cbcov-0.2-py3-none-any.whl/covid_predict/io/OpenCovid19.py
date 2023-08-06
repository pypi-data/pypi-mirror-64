import pandas as pd
import numpy as np

import os.path
import download

from covid_predict.io import default_data_dir
import pandas as pd

#%%

class OpenCovid():
    """
    This class extract the data from the csv created by the opencovid19 initiative. To use it, simply
          
          # grab number of deaths in France
          np_array_with_values, dates = OpenCovid().get_ts_france()
          # grab number of hospitalises in France
          np_array_with_values, dates = OpenCovid().get_ts_france(label="hospitalises")

          # grab number of deaths in départements Paris (75)
          np_array_with_values, dates = OpenCovid().get_ts_departement(code=75)
          # grab number of deaths in Région Grand-Est
          np_array_with_values, dates = OpenCovid().get_ts_region(code='44', label="deces"))  

    Possible labels are:
            "deces"
            "reanimation"
            "hospitalises"
            "gueris"
            "depistes"


    Possible values for the source (src);
            "agences-regionales-sante"
            "sante-publique-france"
            "ministere-sante"
            "lperez31-historical-data"
            "prefectures"
            "sante-publique-france-data"
            "opencovid19-fr"

    The French départements are (code):
            "01": Ain
            "02": Aisne
            "04": Alpes-de-Haute-Provence
            "05": Hautes-Alpes
            "06": Alpes-Maritimes
            "07": Ardèche
            "08": Ardennes
            "10": Aube
            "11": Aude
            "12": Aveyron
            "13": Bouches-du-Rhône
            "14": Calvados
            "16": Charente
            "17": Charente-Maritime
            "18": Cher
            "19": Corrèze
            "21": Côte-d'Or
            "22": Côtes-d'Armor
            "23": Creuse
            "24": Dordogne
            "25": Doubs
            "26": Drôme
            "27": Eure
            "28": Eure-et-Loir
            "29": Finistère
            "2A": Corse-du-Sud
            "2B": Haute-Corse
            "30": Gard
            "33": Gironde
            "34": Hérault
            "35": Ille-et-Vilaine
            "36": Indre
            "37": Indre-et-Loire
            "38": Isère
            "39": Jura
            "40": Landes
            "41": Loir-et-Cher
            "42": Loire
            "44": Loire-Atlantique
            "45": Loiret
            "47": Lot-et-Garonne
            "49": Maine-et-Loire
            "50": Manche
            "51": Marne
            "52": Haute-Marne
            "53": Mayenne
            "54": Meurthe-et-Moselle
            "55": Meuse
            "56": Morbihan
            "57": Moselle
            "58": Nièvre
            "59": Nord
            "60": Oise
            "61": Orne
            "62": Pas-de-Calais
            "63": Puy-de-Dôme
            "64": Pyrénées-Atlantiques
            "67": Bas-Rhin
            "68": Haut-Rhin
            "69": Rhône
            "70": Haute-Saône
            "71": Saône-et-Loire
            "72": Sarthe
            "73": Savoie
            "74": Haute-Savoie
            "75": Paris
            "76": Seine-Maritime
            "77": Seine-et-Marne
            "78": Yvelines
            "79": Deux-Sèvres
            "80": Somme
            "81": Tarn
            "82": Tarn-et-Garonne
            "83": Var
            "84": Vaucluse
            "85": Vendée
            "86": Vienne
            "86": Vienne
            "87": Haute-Vienne
            "88": Vosges
            "89": Yonne
            "89": Yonne
            "90": Territoire de Belfort
            "91": Essonne
            "92": Hauts-de-Seine
            "93": Seine-Saint-Denis
            "94": Val-de-Marne
            "95": Val-d'Oise


    The french Région are coded  as (code keyword arg):
            "REG-01": "Guadeloupe",
            "REG-02": "Martinique",
            "REG-03": "Guyane",
            "REG-04": "La Réunion",
            "REG-06": "Mayotte",
            "REG-11": "Île-de-France",
            "REG-24": "Centre-Val de Loire",
            "REG-27": "Bourgogne-Franche-Comté",
            "REG-28": "Normandie",
            "REG-32": "Hauts-de-France",
            "REG-44": "Grand Est",
            "REG-52": "Pays de la Loire",
            "REG-53": "Bretagne",
            "REG-75": "Nouvelle-Aquitaine",
            "REG-76": "Occitanie",
            "REG-84": "Auvergne-Rhône-Alpes",
            "REG-93": "Provence-Alpes-Côte d'Azur",
            "REG-94": "Corse"
    """
    def __init__(self):
        self.url="https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/"
        self.files_names = "chiffres-cles.csv"
        self.files_labels = "chiffres-cles"
        self.sep = ";"
        self.index_col = 2

        self.df = self._get_csv()
        self.df.drop(columns=['source_url', "source_archive"], inplace=True)
        self.parmaille = {maille: self._normalize(self.df[self.df['maille_code'] == maille]) for maille in pd.unique(self.df['maille_code'])}
        # for key, value in self.parmaille.items() :
            # print(key)
        for key, value in self.parmaille['DEP-75'].items() :
            print(key)

    def __str__(self):
        return "This class grap data from www.data.gouv.fr and get relevant times series."

    def _normalize(self, df):
        return {source : df[self.df['source_type'] == source] for source in pd.unique(self.df['source_type'])}

    def save_csv(self, fname=default_data_dir + "saved_OpenCovid.csv"):
        return self.df.to_cvs(fname)

    def save_raw_csv(self, dirname=default_data_dir):
        download(self.url + self.files_names, os.path.join(dirname, self.files_names), replace=False)

    def _get_csv(self):
        """
            The dataFrame lines are indexed with the dates...
        """
        return pd.read_csv(self.url + self.files_names, parse_dates=['date'], date_parser=pd.to_datetime)

    def get_ts_france(self, label=["deces"], src='ministere-sante'):
        source = self.parmaille['FRA'][src]
        # print(self.parmaille['FRA'][src])
        return source[label].to_numpy(dtype="int64").flatten(), source['date'].to_list()

    def get_ts_departement(self, code='34', label=["deces"], src='agences-regionales-sante'):
        source = self.parmaille['DEP-' + str(code)][src]
        print(source)
        print(source.index)
        print(source.columns)
        return source[label].to_numpy(dtype="int64").flatten(), source['date'].to_list()

    def get_ts_region(self, code='34', label=["deces"], src='agences-regionales-sante'):
        source = self.parmaille['REG-' + str(code)][src]
        return source[label].to_numpy(dtype="int64").flatten(), source['date'].to_list()

    def get_ts_world(self, country='', label=["deces"]):
        source = self.parmaille['WORLD'][src]
        return source[label].to_numpy(dtype="int64").flatten(), source['date'].to_list()


if __name__ == "__main__":
    tmp =OpenCovid()

    print("Number of deaths in france (src: ministere de la Santé):")
    print(tmp.get_ts_france(label="deces", src='ministere-sante'))  

    # print(tmp.get_ts_france(label="deces", src='sante-publique-france')[0])
    # print(tmp.get_ts_france(label="deces", src='opencovid19-fr')[0])

    # print(tmp.get_ts_france(label="reanimation", src='ministere-sante')[0])  
    # print(tmp.get_ts_france(label="reanimation", src='sante-publique-france')[0])
    # print(tmp.get_ts_france(label="reanimation", src='opencovid19-fr')[0])

    # print(tmp.get_ts_france(src='lperez31-historical-data')) # vide
    # print(tmp.get_ts_france(src='prefectures')) # vide
    # print(tmp.get_ts_france(src='sante-publique-france-data')) #vide
    # print(tmp.get_ts_france(src='agences-regionales-sante')) # vide


    # print(tmp.get_ts_departement(code='34', label="deces", src='ministere-sante')[0])  # vide
    # print(tmp.get_ts_departement(code='34', label="deces", src='sante-publique-france')[0]) #vide 
    # print(tmp.get_ts_departement(code='34', label="deces", src='opencovid19-fr')[0]) #vide

    # print(tmp.get_ts_departement(code='34', label="deces", src='agences-regionales-sante'))  
    # print(tmp.get_ts_departement(code='34', label="reanimation", src='agences-regionales-sante'))  
    # print(tmp.get_ts_departement(code='21', label="deces", src='agences-regionales-sante'))  
    # print(tmp.get_ts_departement(code='75', label="deces", src='agences-regionales-sante'))  

    print("\n\nNumber of deaths in Grand-Est (src: ARS):")
    print(tmp.get_ts_region(code='44', label="deces", src='agences-regionales-sante'))  
    # print(tmp.get_ts_region(code='44', label="reanimation", src='agences-regionales-sante'))  

    # print(tmp.get_ts_departement(dep='34', label="deces", src='prefectures'))  # vide
    # print(tmp.get_ts_departement(dep='21', label="deces", src='prefectures'))  # vide
    # print(tmp.get_ts_departement(dep='75', label="deces", src='prefectures'))  # vide
