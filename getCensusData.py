import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from tqdm import tqdm
import json # for saving dictionaries


dataPath = "./data/decennial_2010/"

urls = ["https://api.census.gov/data/2010/dec/sf1/variables.html",
        "https://api.census.gov/data/2000/sf1/variables.html",
        "https://api.census.gov/data/1990/sf1/variables.html"]

# scrape the webpages for all available
# variables
src_2010 = requests.get(urls[0]).content
src_2000 = requests.get(urls[1]).content
src_1990 = requests.get(urls[2]).content

print("Websites fetched!")

soup_2010 = BeautifulSoup(src_2010, 'lxml')
soup_2000 = BeautifulSoup(src_2000, 'lxml')
soup_1990 = BeautifulSoup(src_1990, 'lxml')

print("soupified...")

# grab all of the variables from the table
# and turn them into dataframes
table_2010 = soup_2010.find_all('table')
table_2000 = soup_2000.find_all('table')
table_1990 = soup_1990.find_all('table')

df_2010 = pd.read_html(str(table_2010))[0]
df_2000 = pd.read_html(str(table_2000))[0]
df_1990 = pd.read_html(str(table_1990))[0]

print("DataFrames created...")


# create variable lookup dictionary to be used later
lookup_2010 = {}
for i in tqdm(range(df_2010.shape[0])):
    lookup_2010[df_2010.loc[i, 'Name']] = df_2010.loc[i, 'Label']

lookup_2000 = {}
for i in tqdm(range(df_2000.shape[0])):
    lookup_2000[df_2000.loc[i, 'Name']] = df_2000.loc[i, 'Label']

lookup_1990 = {}
for i in tqdm(range(df_1990.shape[0])):
    lookup_1990[df_1990.loc[i, 'Name']] = df_1990.loc[i, 'Label']


# save the dictionaries
with open('./data/decennial_2010/variable_summary.json', 'w') as f:
    json.dump(lookup_2010, f)
with open('./data/decennial_2000/variable_summary.json', 'w') as f:
    json.dump(lookup_2000, f)
with open('./data/decennial_1990/variable_summary.json', 'w') as f:
    json.dump(lookup_1990, f)


# define variable lists:
# use list comprehension
vars_90 = [var if(var != "for" and var != "in" and var != "ucgid") else "" for var in df_1990.loc[:, 'Name']]
vars_00 = [var if(var != "for" and var != "in" and var != "ucgid") else "" for var in df_2000.loc[:, 'Name']]
vars_10 = [var if(var != "for" and var != "in" and var != "ucgid") else "" for var in df_2010.loc[:, 'Name']]

# filter out the "" from the for and in names
vars_90 = list(filter(None, vars_90))
vars_00 = list(filter(None, vars_00))
vars_10 = list(filter(None, vars_10))



# generate data for 2010
# ------------------------------------------------------------------------------------------------------------
HOST = "https://api.census.gov/data"
year = "2010"
dataset = "dec/sf1"
base_url = "/".join([HOST, year, dataset])


print("Generating data for ", base_url)

# create request dictionary
predicates = {}
predicates["key"] = "97d54f0b2bec96ce45749d21afa620949a6cd273"
predicates["for"] = "tract"
predicates["in"] = "state:48;county:*"

# generate dictionary with state codes
# http://mcdc.missouri.edu/applications/geocodes/?state=00
states = {"01": "Alabama",
          "02": "Alaska ",
          "04": "Arizona",
          "05": "Arkansas",
          "06": "California",
          "08": "Colorado",
          "09": "Connecticut",
          "10": "Delaware",
          "11": "District of Columbia",
          "12": "Florida",
          "13": "Georgia",
          "15": "Hawaii",
          "16": "Idaho",
          "17": "Illinois",
          "18": "Indiana",
          "19": "Iowa",
          "20": "Kansas",
          "21": "Kentucky",
          "22": "Louisiana",
          "23": "Maine",
          "24": "Maryland",
          "25": "Massachusetts",
          "26": "Michigan",
          "27": "Minnesota",
          "28": "Mississippi",
          "29": "Missouri",
          "30": "Montana",
          "31": "Nebraska",
          "32": "Nevada",
          "33": "New Hampshire",
          "34": "New Jersey",
          "35": "New Mexico",
          "36": "New York",
          "37": "North Carolina",
          "38": "North Dakota",
          "39": "Ohio",
          "40": "Oklahoma",
          "41": "Oregon",
          "42": "Pennsylvania",
          "72": "Puerto Rico",
          "44": "Rhode Island",
          "45": "South Carolina",
          "46": "South Dakota",
          "47": "Tennessee",
          "48": "Texas",
          "49": "Utah",
          "50": "Vermont",
          "51": "Virginia",
          "53": "Washington",
          "54": "West Virginia",
          "55": "Wisconsin",
          "56": "Wyoming"
}


# ------------------------------------------------------------------------------------------------------------
# loop over states to generate the data
for key, value in states.items():
    tqdm.write("Working on {}".format(value))
    predicates = {}
    predicates["key"] = "97d54f0b2bec96ce45749d21afa620949a6cd273"
    predicates["for"] = "tract"
    predicates["in"] = "state:{};county:*".format(key)

    N = len(vars_10)
    slices = list(np.arange(0, N, 50))
    slices.append(N-1)

    df_state = pd.DataFrame()

    for i in tqdm(range(1, len(slices))):
        get_vars = vars_10[slices[i-1]:slices[i]]
        predicates["get"] = ",".join(get_vars)

        r = requests.get(base_url, params=predicates)
        if(r.status_code!= 200):
            print("Error retrieving data: {}".format(r.status_code))

        names = r.json()[0]
        data = r.json()[1:]
        df = pd.DataFrame(data=data, columns=names)

        for col in df.columns:
            if col not in df_state.columns:
                df_state[col] = df[col]

    df_state.to_csv("./data/decennial_2010/{}_census.csv".format(value))



