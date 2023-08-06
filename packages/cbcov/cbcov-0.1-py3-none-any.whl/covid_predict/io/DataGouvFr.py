import pandas as pd
import numpy as np

import os.path
import download

default_data_dir =  os.path.dirname(os.path.abspath(__file__)) + (os.path.sep + '..')*2


class DataGouvFr():
    def __init__(self):
        self.url = "https://www.data.gouv.fr/fr/datasets/r/"
        self.files_names = "63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
        self.files_labels = "données_complètes"
        self.sep = ";"
        self.index_col = 2

        self.df = self._get_csv()

        # remove sexe variables : 0 M+F; 1 = M; 2 =F
        self.df = self.df.query("sexe == " + str(0))  # sum male/female
        self.df.drop(columns=["sexe"], inplace=True)

    def __str__(self):
        return "This class grap data from www.data.gouv.fr and get relevant times series."

    def save_csv(self, fname=default_data_dir + "saved_DataGouvFr.csv"):
        return self.df.to_cvs(fname)

    def save_raw_csv(self, dirname=default_data_dir):
        download(self.url + self.files_names, os.path.join(dirname, self.files_names), replace=False)

    def _get_csv(self):
        """
            The dataFrame lines are indexed with the dates...
        """
        return pd.read_csv(self.url + self.files_names, parse_dates=True, sep=self.sep, index_col=2)

    def get_ts_france(self, label=["hosp",  "rea",  "rad",  "dc"]):
        return np.array([self.df.loc[i, label].sum() for i in self.df.index.unique()]).flatten(), self.df.index.unique()

    def get_ts_departement(self, dep=34, label=["hosp",  "rea",  "rad",  "dc"]):
        df = self.df.loc[self.df.loc[:, 'dep'] == str(dep), 'dc']
        return df.to_numpy().flatten(), df.index
