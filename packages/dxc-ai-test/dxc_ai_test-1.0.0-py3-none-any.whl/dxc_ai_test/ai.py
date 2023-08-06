import json
import pandas as pd
import doctest #documenting data stories
import requests #reading data
import datetime
from pymongo import MongoClient #MongoDB
from auto_ml import Predictor #ML models
from sklearn.model_selection import train_test_split
import os
import pickle #serializing models
import Algorithmia
from Algorithmia.errors import AlgorithmException
import shutil #serializing models
import urllib.parse #input data
#from git import Git, Repo, remote
from IPython.display import YouTubeVideo
from IPython.core.magic import register_line_cell_magic
import urllib.request, json #input data
from flatten_json import flatten #json input data
import janitor #data cleaning
from ftfy import fix_text #data cleaning
import nltk #data cleaning
#nltk.download('punkt') #data cleaning
import scrubadub #data cleaning
import arrow #normalizing dates
import numpy as np
from sklearn.base import TransformerMixin #impute missing data
from sklearn.model_selection import train_test_split #model training
from yellowbrick.features import Rank2D #exploring raw data
import matplotlib.pyplot as plt #exploring raw data
from datacleaner import autoclean #data cleaning
#from pydataset import data
import io #read data from local files
#from google.colab import files #read data from local files
import missingno as msno #gauge dataset completeness
import seaborn as sns #data exploration, distribution plotting
from pandas.api.types import is_numeric_dtype #data exploration, distribution plotting
import math #data exploration, distribution plotting


#FLATTENING FILE

def flatten_json_into_dataframe(json_data):
  #flatten the nested JSON data into a data frame
  json_data_flattened = [flatten(d) for d in json_data]
  df = pd.DataFrame(json_data_flattened)
  return(df)

class DataFrameImputer(TransformerMixin):
    def __init__(self):
        """Impute missing values.

        Columns of dtype object are imputed with the most frequent value 
        in column.

        Columns of other types are imputed with mean of column.

        """
    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)

#READING FILE

def read_data_frame_from_remote_json(json_url):
    with urllib.request.urlopen(json_url) as url:
        json_data = json.loads(url.read().decode())
    df = flatten_json_into_dataframe(json_data)
    return(df)


#CLEANING FILE

def clean_dataframe(df, impute = False, text_fields = [], date_fields = [], numeric_fields = [], categorical_fields = []):

  clean_df = (
    df
    #make the column names lower case and remove spaces
    .clean_names()

    #remove empty columns
    .remove_empty()

    #remove empty rows and columns
    .dropna(how='all')
  )

  #remove harmful characters. remove personal identifiers. make lowercase
  for field in text_fields:
    clean_df[field] = clean_df[field].apply(fix_text)
    clean_df[field] = clean_df[field].apply(scrubadub.clean, replace_with='identifier')
    clean_df[field] = clean_df[field].str.lower()
  
  #impute missing values
  if impute:
    clean_df = DataFrameImputer().fit_transform(clean_df)

  #standardize the format of all date fields
  for field in date_fields:
    clean_df[field] = clean_df[field].apply(arrow.get)

  #make sure all numeric fields have the proper data type
  for field in numeric_fields:
    clean_df[field] = pd.to_numeric(clean_df[field])
  
  #make sure all categorical variables have the proper data type
  for field in categorical_fields:
    clean_df[field] = clean_df[field].astype('category')

  return(clean_df)

#VISUALIZATION

#display the correlations in pairwise comparisons of all features
def explore_features(df):
  df_copy = df.copy()

  #for some reason, the visualize doesn't accept categorical
  #variables. those have to be converted to strings
  for (col,data) in df_copy.iteritems():
    if df_copy[col].dtype.name == "category":
      df_copy[col] = df_copy[col].astype(str)

  numeric_df = autoclean(df_copy)
  visualizer = Rank2D(algorithm="pearson")
  visualizer.fit_transform(numeric_df)
  visualizer.poof()

#display a visual representation of missing fields in the given data
def visualize_missing_data(df):
  msno.matrix(df, figsize=(15,8))

#plot the distribution of values of each field in the given data
def plot_distributions(df):

  #set plot style
  sns.set(style="darkgrid")

  features = len(df.columns)

  #determine the number of columns in the plot grid and the width and height of each plot
  grid_cols = 3
  plot_width = 5
  plot_height = 3

  #determine the width of the plot grid and number of rows
  grid_width = plot_width * grid_cols
  num_rows = math.ceil(features/grid_cols)

  #determine the width of the plot grid
  grid_height = plot_height * num_rows

  #lay out the plot grid
  fig1 = plt.figure(constrained_layout=True, figsize = (grid_width,grid_height))
  gs = fig1.add_gridspec(ncols = grid_cols, nrows = num_rows)

  #step through the dataframe and add plots for each feature
  current_column = 0
  current_row = 0
  for col in df.columns:

    #set up a plot
    f1_ax1 = fig1.add_subplot(gs[current_row, current_column])
    f1_ax1.set_title(col)

    #create a plot for numeric values
    if is_numeric_dtype(df[col]):
      sns.distplot(df[col], ax = f1_ax1).set_xlabel('')
    
    #creare a plot for categorical values
    if df[col].dtype.name == "category":
      sns.countplot(df[col], ax = f1_ax1, order = df[col].value_counts().index).set_xlabel('')

    #move to the next column
    current_column +=1

    #determine if it is time to start a new row
    if current_column == grid_cols:
      current_column = 0
      current_row +=1

def convert_dates_from_arrow_to_string(df, arrow_date_fields):
    for field in arrow_date_fields:
        df[field] = df[field].apply(format)
    return(df)

def write_raw_data(data_layer, raw_data):
    ##convert your raw data into writable data by converting Arrow dates to strings
    arrow_date_fields = ['date_fleet_doc_entered', 'purchasing_bid_date', 'date_bid_closed', 'date_po_awarded']
    writable_raw_data = convert_dates_from_arrow_to_string(raw_data, arrow_date_fields)
    
    #connect to the data layer
    client = MongoClient(data_layer["connection_string"])
    
    #start a data collection, build a database, insert the raw data
    db = client[data_layer["database_name"]][data_layer["collection_name"]]
    db.insert_many(writable_raw_data.to_dict('records'))
    return db

def access_data_from_pipeline(db, pipe):
    data = db.aggregate(pipeline=pipe)
    data = list(data)
    df = pd.io.json.json_normalize(data)

    return df

# define the general class of models
class model:
    __model = []
    def build(self, meta_data): raise NotImplementedError()
    def train_and_score(self, data): raise NotImplementedError()
    def interpret(self): raise NotImplementedError()
    def python_object(): raise NotImplementedError()

    @staticmethod
    def meta_data_key(meta_data, value):
        key_list = list(meta_data.keys()) 
        val_list = list(meta_data.values()) 
  
        return key_list[val_list.index(value)] 

#define the model lifecycle
def run_experiment(design):
    design["model"].build(design["meta_data"])
    design["model"].train_and_score(design["data"], design["labels"])
    design["model"].interpret()
    return design["model"].python_object()

# define a prediction model
class prediction(model):

    @property
    def estimator(self):
        raise NotImplementedError()

    def build(self, meta_data):
        self.__model = Predictor(type_of_estimator=self.estimator, column_descriptions=meta_data)
        self.__label = self.meta_data_key(meta_data, "output")

    def train_and_score(self, data, labels):
    # create training and test data
        training_data, test_data = train_test_split(data, test_size=0.2)

    # train the model
        self.__model.train(training_data, verbose=False, ml_for_analytics=False)
  
    # score the model
        self.__model.score(test_data, test_data[self.__label], verbose=0)
  
    def interpret(self):
        pass
  
    def python_object(self):
        return self.__model

class regression(prediction):
    @property
    def estimator(self):
        return("regressor")

# define a regressor model
class classification(prediction):
    @property
    def estimator(self):
        return("classifier")


def run_experiment(experiment_design):
    # define the general class of models

    experiment_design["model"].build(experiment_design["meta_data"])
    experiment_design["model"].train_and_score(experiment_design["data"], experiment_design["labels"])
    experiment_design["model"].interpret()
      
    return experiment_design["model"].python_object()

    
