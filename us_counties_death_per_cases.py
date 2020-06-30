# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:54:28 2020

https://plotly.com/python/county-choropleth/?fbclid=IwAR1xOTSniBA_d1okZ-xEOa8eEeapK8AFTgWILshAnEvfLgJQPAhHgsVCIBE
https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset
"""
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import plotly
from plotly.offline import plot

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
                 dtype={"fips": str})

print(df.head)
print(df.shape)
print(df["date"][df.shape[0] - 1])
current_date = df["date"][df.shape[0] - 1] # 6/28/2020



specific_date_df = pd.DataFrame(data=None, columns=list(df.columns.values))

for index, row in df.iterrows():
    if row["date"] == current_date:
        specific_date_df.loc[df.index[index]] = df.iloc[index]
    
print(specific_date_df) # has all data for current date
# 3067 x 6


specific_date_df = specific_date_df.copy()

IFR_list = []
for index, row in specific_date_df.iterrows():
    if row["cases"] > 0:
        IFR = row["deaths"] / row["cases"]
        IFR_list.append(IFR)
    else:
        IFR_list.append(0)

specific_date_df["IFR"] = IFR_list

print(specific_date_df)

specific_date_df = specific_date_df.reset_index(drop=True)
specific_date_Georgia_df = pd.DataFrame(data=None, columns=list(specific_date_df.columns.values))
print(specific_date_df)
print(specific_date_Georgia_df)


# # for picking out a specific state, in this case Georgia
# state = "Georgia"
# index_counter = 0
# for index, row in specific_date_df.iterrows():
#     # print(index)
#     if row["state"] == state:
#         # print("yes")
#         # print(index)
#         # print(copy_new_df.index[index])
#         specific_date_Georgia_df.loc[index_counter] = specific_date_df.iloc[index]
#         index_counter += 1
#         # print(index_counter)
# print(specific_date_Georgia_df) # has all data for current date


with urlopen('https://gist.githubusercontent.com/wavded/1250983/raw/bf7c1c08f7b1596ca10822baeb8049d7350b0a4b/stateToFips.json') as response:
    fips_states = json.load(response)
    
# print(fips_states)
# print(fips_states.keys())
# print()
fips_states_keys = list(fips_states.keys())
# print(fips_states_keys)
fips_states_values = list(fips_states.values())
# print()
# print(fips_states_values)

print(fips_states_keys)  
fips_states_keys = [w.replace('ogia', 'orgia') for w in fips_states_keys]
print(fips_states_keys)


#%%

# these are in the data from kaggle but not in the geojson
specific_date_df = specific_date_df[specific_date_df["state"] != "Northern Mariana Islands"]
specific_date_df = specific_date_df[specific_date_df["state"] != "Virgin Islands"]
specific_date_df = specific_date_df[specific_date_df["state"] != "Puerto Rico"]
specific_date_df = specific_date_df[specific_date_df["state"] != "Guam"]


for state, state_id in zip(fips_states_keys, fips_states_values):
    specific_date_df = specific_date_df.replace(state, state_id)
print(specific_date_df)
#%%
states_only_df = pd.DataFrame()
list_state_count = []
list_str_states = list(specific_date_df["state"].unique())
# print(list_str_states)
for id_ in list_str_states:
    total = 0
    for index, row in specific_date_df.iterrows():
        if row["state"] == id_:
            # print(id_)
            total += row["cases"]
    list_state_count.append(total)
            
    # break

print(list_state_count)
print(len(list_state_count))
states_only_df["per_state_count"] = list_state_count
states_only_df["state_id"] = list_str_states
states_only_df["state_name"] = fips_states_keys
print(states_only_df)


#%%

# # Per county geojson
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

# print(counties["features"][0]["properties"]["STATE"])
# print(len(counties["features"])) #3221

#%%
with open('gz_2010_us_040_00_20m.json') as response:
    states_mapping = json.load(response)


print(states_mapping["features"][0]["properties"]["STATE"])
print(len(states_mapping["features"])) #3221

#%%

pop_states = pd.read_csv("population_states_2019.txt", header=0)
# print(pop_states["State"])

# print(states_only_df)

pop_list = []
for state in states_only_df["state_name"]:
    for i,row in pop_states.iterrows():
        if row["State"] == state:
            pop_list.append(row["Population"])
            
states_only_df["state_pop"] = pop_list
# print(pop_list)
# print(len(pop_list))

#%%
per100k = []
for pop, count in zip(states_only_df["state_pop"], states_only_df["per_state_count"]):
    per100k.append(100000 * (count/pop))
    
states_only_df["per100k"] = per100k
print(states_only_df)

#%%


fig = px.choropleth(states_only_df, geojson=states_mapping,
                           locations='state_id', 
                           color='per100k',
                           color_continuous_scale="Viridis",
                           # range_color=(0, 10),
                           # locationmode = 'USA-states',
                           featureidkey = "properties.STATE",
                           hover_name = "state_name",
                           scope="usa",
                           labels={'per100k':'cases per 100k'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
plot(fig)



