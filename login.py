import panel as pn
import pandas as pd
import hvplot.pandas
import warnings
import mysql.connector
import json
import datetime as dt
import os



def returnLogDetails():

    host_socasp = "192.168.56.1"
    user_socasp = 'dondonedmond'
    password_socasp = 'toor'
    database_socasp = 'socasp'

    return host_socasp, user_socasp, password_socasp, database_socasp