from flask import Flask, render_template, jsonify,request
import psycopg2
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import datetime
from time import mktime
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load variables from .env file
load_dotenv('local.env')

host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

# database connection parameters
db_params = {
    "host": host,
    "port": port,
    "database": database,
    "user": user,
    "password": password
}

# retrieve data from the PostgreSQL database based on start date and end date
def get_data(table_name,start_date,end_date):

    # Connect to the PostgreSQL database server
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Query to retrieve data from the database
    query = "SELECT * FROM " + table_name
    if start_date!="" and end_date!="":
        query += f" WHERE time BETWEEN '{start_date}' AND '{end_date}'"
    elif start_date!="" and end_date=="":
        query += f" WHERE time >= '{start_date}'"
    elif end_date!="" and start_date=="":
        query += f" WHERE time <= '{end_date}'"
    cur.execute(query)

    # Fetch all rows from the result set
    data = cur.fetchall()

    # Close the cursor and connection to so the server can allocate
    cur.close()
    conn.close()
    return data


# Convert the data into a dictionary
def get_dict(name,data):

    # Convert the data into different lists of time and value
    time = [row[0] for row in data]
    value = [row[1] for row in data]

    # Convert the time into unix timestamp for the graph
    unix_timestamp_list = [(int(mktime(dt.timetuple()))*1000) for dt in time]

    dict = {name: value,'time':unix_timestamp_list}
    return dict


# API route to get the data
@app.route('/get_value', methods=['POST'])
def get_value():

    print("---------------Getting data")
    # Get the start and end date from the request
    dates = request.get_json()
    start_date = dates['start']
    end_date = dates['end']

    dict = {}

    # Get data for each parameter
    name = "A"
    table_name = 'A'
    data = get_data(table_name,start_date,end_date)
    dict_A = get_dict(name,data)

    name = "B"
    table_name = 'B'
    data = get_data(table_name,start_date,end_date)
    dict_B = get_dict(name,data)

    name = "C"
    table_name = 'C'
    data = get_data(table_name,start_date,end_date)
    dict_C = get_dict(name,data)

    name = "D"
    table_name = 'D'
    data = get_data(table_name,start_date,end_date)
    dict_D = get_dict(name,data)


    # Create a single dictionary of all parameters to return
    dict['A'] = dict_A
    dict['B'] = dict_B
    dict['C'] = dict_C
    dict['D'] = dict_D

    
    # Return the dictionary as an API response
    return jsonify(dict)


# dashboard route
@app.route('/')
def dashboard():
    # Retturn a template with the search form
    print("Rendering dashboard")
    return render_template('index.html')



def execute():
    print("Executing application")
    app.run(host='0.0.0.0',port=8888)
