import os
import numpy as np
##import cv2 as cv2
import pydicom
import matplotlib
from os import walk
#voir PIL
#import nibabel as nib
from pandas import ExcelWriter
from pandas import ExcelFile
#import xlwt
import sys
##import cv2 as cv2
import numpy.ma as ma
import matplotlib.pyplot as plt
import glob
import pandas as pd
from pydicom.data import get_testdata_files
from tqdm import tqdm
from Classe.class_chemin import Config, config

from datetime import datetime



class DCMMetaExtractor():
    def __init__(self):
        self.param = Config(config)
        self.output_DF = None
        self.metadata = None
        self.NAME = None
        self.SEXE = None
        self.STUDY_DATE = None
        self.MODALITY = None
        self.STUDY_DESCRIPTION = None
        self.PATIENT_BIRTHDAY = None
        self.Age = None
        ##self.li_dict = None

    def generate_dataframe(self):

        self.NAME = []
        self.SEXE = []
        self.MODALITY = []
        self.STUDY_DESCRIPTION = []
        self.PATIENT_BIRTHDAY = []
        self.STUDY_DATE = []
        self.Age = []
        for root, dirs, files in walk(self.param.startpath):
            for file in files:
                file_path_dcm = os.path.join(root, file)
                if file_path_dcm.endswith(".dcm"):
                    print(file)
                    ds = pydicom.dcmread(file_path_dcm, force=True)
                    self.metadata = ds
                    print(ds)
                    self.NAME.append(ds.PatientID)
                    self.SEXE.append(ds.PatientSex)
                    self.MODALITY.append(ds.Modality)
                    self.STUDY_DATE.append(ds.StudyDate)
                    self.PATIENT_BIRTHDAY.append(ds.PatientBirthDate)
                    self.STUDY_DESCRIPTION.append(ds.StudyDescription)
                    self.Age.append(int(str(ds.StudyDate[0:4])) - int(str(ds.PatientBirthDate[0:4])))

                columns = [self.NAME, self.SEXE, self.MODALITY, self.STUDY_DATE, self.PATIENT_BIRTHDAY,
                           self.STUDY_DESCRIPTION, self.Age]

        self.output_DF = pd.DataFrame(columns)

    def transpose(self):
        self.output_DF = self.output_DF.transpose()

    def rename_column(self):
        self.output_DF.rename(columns={0: 'PatientID', 1: 'Sexe', 2: 'Modality', 3: 'Study_Date',
                                       4: 'Birthday', 5: 'Study_Description', 6: "Age"}, inplace=True)

    def fihier_anonymisation(self):
        self.df_excel = pd.read_excel(self.param.fichier_anonymisation)

    def merge_data(self):
        self.df = pd.merge(self.output_DF, self.df_excel, on="PatientID", how='left')

    def netoyage_data(self):
        self.df = self.df.drop(["PatientID", "Nom des patients"],axis=1)
        self.df["Sexe"] = self.df['Sexe'].replace({'M': 0, 'F': 1})
        self.df["Study_Date"] = pd.to_datetime(self.df["Study_Date"])
        self.df["Birthday"] = pd.to_datetime(self.df["Birthday"])
        self.df["Study_Date"] = self.df["Study_Date"].dt.strftime("%Y-%m")
        self.df["Birthday"] = self.df["Birthday"].dt.strftime("%Y-%m")



if __name__ == '__main__':

    test = DCMMetaExtractor()
    test.generate_dataframe()
    test.transpose()
    test.fihier_anonymisation()
    test.rename_column()
    test.merge_data()
    test.netoyage_data()



##test.df["Study_Date"]=pd.to_datetime(test.df["Study_Date"],format='%Y-%m')

##for i in range(0,len(test.df["PatientID"]),1):
    ##date.append(str(test.df["PatientID"][i])[0:4])

 ## def merge_data(self):
        ##self.df_excel = pd.read_excel(self.parm.fichier_anonymisation)
"""
test.output_DF = test.output_DF.transpose()
    test.output_DF.rename(columns={0: 'PatientId', 1: 'Sexe', 2: 'Modality', 3: 'Study_Date',
                                     4 : 'Birthday', 5: 'Study_Description', 6: "Age"}, inplace=True)
###  test.output_DF = test.output_DF.astype({"Study_Date":'int64',"Birthday":'int64'})

## test.output_DF['Age'] = test.output_DF['Study_Date'] - test.output_DF['Birthday']
##data["Salary"]= data["Salary"].astype(int)

##for i in range(0,len(test.output_DF["PatientId"]),1):
    ##age.append(str(test.output_DF["PatientId"][i])[0:4])

# dummies = pd.get_dummies(df['Sex']).rename(columns=lambda x: 'Sex_' + str(x))
## test.output_DF = pd.concat([test.output_DF,dummies], axis = 1)
## test.output_DF.corr()
"""