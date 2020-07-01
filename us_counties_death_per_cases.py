# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:54:28 2020

https://plotly.com/python/county-choropleth/?fbclid=IwAR1xOTSniBA_d1okZ-xEOa8eEeapK8AFTgWILshAnEvfLgJQPAhHgsVCIBE
https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset

better census data
https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/
"""
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import plotly
from plotly.offline import plot
import os
import math

if not os.path.exists("images_counties"):
    os.mkdir("images_counties")
    
with urlopen('https://gist.githubusercontent.com/wavded/1250983/raw/bf7c1c08f7b1596ca10822baeb8049d7350b0a4b/stateToFips.json') as response:
    fips_states = json.load(response)       
fips_states_keys = list(fips_states.keys())
fips_states_values = list(fips_states.values())
fips_states_keys = [w.replace('ogia', 'orgia') for w in fips_states_keys]
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
dfmain = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
                 dtype={"fips": str})
# print(dfmain.head)
# print(dfmain.shape)
# print(dfmain["date"][dfmain.shape[0] - 1])
# print(dfmain["date"][1])
# current_date = dfmain["date"][dfmain.shape[0] - 1] # 6/29/2020, or yesterday
# current_date = df["date"][10] # 6/29/2020
#%%
def load_data(when = 0, yesterday=True):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
                 dtype={"fips": str})
    current_date = ''
    if yesterday:
        current_date = df["date"][df.shape[0] - 1] # 6/29/2020
    else:
        current_date = df["date"][when]
        
    return df, current_date


def make_df_for_date(input_date, df):

    specific_date_df = pd.DataFrame(data=None, columns=list(df.columns.values))
    
    for index, row in df.iterrows():
        if row["date"] == input_date:
            specific_date_df.loc[df.index[index]] = df.iloc[index]
        
    # print(specific_date_df) # has all data for current date
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
    
    # print(specific_date_df)
    
    specific_date_df = specific_date_df.reset_index(drop=True)
    
    # specific_date_Georgia_df = pd.DataFrame(data=None, columns=list(specific_date_df.columns.values))
    # print(specific_date_df)
    # print(specific_date_Georgia_df)
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
    fips_states_keys = list(fips_states.keys())
    fips_states_values = list(fips_states.values())
    fips_states_keys = [w.replace('ogia', 'orgia') for w in fips_states_keys]
    
    
    
    # these are in the data from kaggle but not in the geojson
    specific_date_df = specific_date_df[specific_date_df["state"] != "Northern Mariana Islands"]
    specific_date_df = specific_date_df[specific_date_df["state"] != "Virgin Islands"]
    specific_date_df = specific_date_df[specific_date_df["state"] != "Puerto Rico"]
    specific_date_df = specific_date_df[specific_date_df["state"] != "Guam"]
    
    
    for state, state_id in zip(fips_states_keys, fips_states_values):
        specific_date_df['state'] = specific_date_df['state'].replace(state, state_id)
    # print(specific_date_df)
    return specific_date_df

#%%
def states_heat_map(specific_date_df):
    "for showing data per state"
    
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
    
    my_file = os.path.join(THIS_FOLDER, 'population_states_2019.txt')
    pop_states = pd.read_csv(my_file, header=0)
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
    
    per100k = []
    for pop, count in zip(states_only_df["state_pop"], states_only_df["per_state_count"]):
        per100k.append(100000 * (count/pop))
        
    states_only_df["per100k"] = per100k
    print(states_only_df)
    
    
    
    with open('gz_2010_us_040_00_20m.json') as response:
        states_mapping = json.load(response)
    
    
    print(states_mapping["features"][0]["properties"]["STATE"])
    print(len(states_mapping["features"])) #3221
    
    # per state
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
    return fig


#%%
def counties_heat_map(specific_date_df, date):
    "for showing data per county"
    
    my_file = os.path.join(THIS_FOLDER, 'all_census_data.csv')
    pop_counties = pd.read_csv(open(my_file))
    
    # print(pop_counties)
    
    county_id = list(pop_counties["COUNTY"])
    state_id = list(pop_counties["STATE"])
    population_per_county = list(pop_counties["POPESTIMATE2019"])
    fips_county_ids = []
    
    for n, c_id in enumerate(county_id):
        if c_id < 10:
            county_id[n] = "00"+str(c_id)
        elif c_id < 100:
            county_id[n] = "0"+str(c_id)
        else:
            county_id[n] = str(c_id)
            
    for n, s_id in enumerate(state_id):
        if s_id < 10:
            state_id[n] = "0"+str(s_id)
        else:
            state_id[n] = str(s_id)
            
    # print(county_id[57])
    # print(state_id[600])
    
    for c,s in zip(county_id, state_id):
        fips_county_ids.append(s + c)
        
    # print(fips_county_ids[1])
    
    # print(len(county_id))
    # print(len(state_id))
    # print(len(fips_county_ids))
    
    
    specific_date_df["county"] = specific_date_df["county"].str.replace('.', '') # DistrictOfColumbia 
    
    
    spec_fips = list(specific_date_df["fips"])
    
    
    odd_balls = [] # unknown county cases
    population_counties_list = []
    # counter = 0
    for spec_fips in spec_fips: 
        boo = True
        for fips_census in fips_county_ids:
            if spec_fips == fips_census:
                population_counties_list.append(population_per_county[fips_county_ids.index(fips_census)]) 
                boo = False
        # counter += 1
        if boo == True:
            population_counties_list.append(1) 
            odd_balls.append(spec_fips) # unknown county cases
            # print(spec_fips)
            
    # print(len(population_counties_list)) # 3065
    # print(population_counties_list)

    
    
    specific_date_df["county_population"] = population_counties_list
    
    
    per100k = []
    for pop, count in zip(specific_date_df["county_population"], specific_date_df["cases"]):
        if pop == 1:
            per100k.append(1)
        else:
            per100k.append(100000 * (count/pop))
        
    specific_date_df["per100k"] = per100k
    # print(specific_date_df)
    # print(per100k)
    
    per10k = []
    for pop, count in zip(specific_date_df["county_population"], specific_date_df["cases"]):
        if pop == 1:
            per10k.append(1)
        else:
            per10k.append(10000 * (count/pop))


    specific_date_df["per10k"] = per10k
    # print(specific_date_df)
    # print(per10k)
    
    # import math
    log10_per10k = []
    for item in per10k:
        # print(item)
        log10_per10k.append(math.log10(item))
    specific_date_df["log10_per10k"] = log10_per10k
    
    # import math
    log10_per100k = []
    for item in per100k:
        # print(item)
        log10_per100k.append(math.log10(item))
    specific_date_df["log10_per100k"] = log10_per100k
    
    
    copy_df = specific_date_df.copy() # this is to remove data from census that is missing from covid
    copy_df = copy_df[copy_df['log10_per100k'] != 0]
    
    # Per county geojson
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    
    # print(counties["features"][0]["properties"]["STATE"])
    # print((counties["features"][0])) #3221
    
    # per county
    fig = px.choropleth(copy_df, geojson=counties,
                               locations='fips', 
                               color='log10_per100k',
                                color_continuous_scale="icefire", # winner
                                # color_continuous_scale="Viridis",
                               # color_continuous_scale="portland",
                                # color_continuous_scale="phase",
                                range_color=(0, 5),
                               # locationmode = 'USA-states',
                               featureidkey = "id",
                               hover_name = "county",
                               scope="usa",
                               labels = {'log10_per100k': 'log10 per 100k pop'}
                              )
    fig.update_layout(margin={"r":5,"t":5,"l":5,"b":5},
                      title_text = '<br><br>Covid-19 Total Cases Per 100k Population Per County<br>Using 2019 Census Estimations<br>'+date
                      )
    # fig.show()
    # plot(fig)
    return fig
#%%
def main():
    #[282519 rows x 6 columns] dfmain.shape[0]
    old_date = ''
    for i in range(dfmain.shape[0]):
        new_date = dfmain["date"][i]
        if i%50 == 0 and new_date != old_date:
            old_date = new_date
            print("Date: ", new_date)
            # df, current_date = load_data(when = i, yesterday=False)
            df, current_date = load_data(when = i, yesterday=False)

            specific_date_df = make_df_for_date(input_date = current_date, df = df)
            fig = counties_heat_map(specific_date_df, new_date)
            # states_heat_map(specific_date_df):
    
            fig.write_image("images_counties/"+new_date+"_county_per100k.png")
        # break
#%%
if __name__ == "__main__":
    main()

#%%
from PIL import Image, ImageDraw
import PIL
import os
images = []
directory = 'C:/Users/karas/.spyder-py3/coronavirus/images_counties'
for filename in os.listdir(directory):
    # print("hi")
    f = Image.open('C:/Users/karas/.spyder-py3/coronavirus/images_counties/'+filename)
    # f = f.save(filename)
    images.append(f)

print(len(images))   

images[0].save('covid_timeline_county_cases.gif',
                save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

#%%
#Graveyard

# def counties_heat_map(specific_date_df, date):
#     "for showing data per county"
    
#     my_file = os.path.join(THIS_FOLDER, 'population_counties_2019.xlsx')
#     pop_counties = pd.read_excel(open(my_file, 'rb'), index_col=None, sep='\t')
    
#     # print(pop_counties)
#     # print(pop_counties["Geographic Area"])
#     # pop_counties["Geographic Area"] = pop_counties["Geographic Area"].map(lambda x: x.lstrip('. ,').rstrip('aAbBcC'))
#     pop_counties["Geographic Area"] = pop_counties["Geographic Area"].str.replace('.', '')
#     pop_counties["Geographic Area"] = pop_counties["Geographic Area"].str.replace(',', '')
#     # pop_counties["Geographic Area"] = pop_counties["Geographic Area"].str.replace('District of Columbia District of Columbia', 'District of Columbia')
#     pop_counties["Geographic Area"] = pop_counties["Geographic Area"].str.replace(' County', '')
#     # pop_counties["Geographic Area"] = pop_counties["Geographic Area"].str.replace(' ', '')
    
#     # print(pop_counties)
    
#     # for value in pop_counties["Geographic Area"]:
#     #     if "District " in value:
#     #         print(value)
#     # for item in pop_counties["Geographic Area"]:
#     #     if "Virginia" in item:
#     #         print(item)
    
#     # print(pop_counties.shape)
#     states_col_for_county_pop = []
#     for index, row in pop_counties.iterrows():
#         one_state = ''
#         for state in fips_states_keys:
#             if state in row["Geographic Area"]:
#                 if row["Geographic Area"].find(state) > 1:
#                     one_state = state
#                     # if one_state == "Distric of Columbia":
#                     #     print("huzzah")
#                 if state == "District of Columbia":
#                     # print("aye")
#                     # print(one_state)
#                     one_state = "District of Columbia"
#         if one_state in row["Geographic Area"]:
#             states_col_for_county_pop.append(one_state)
#     # print(len(states_col_for_county_pop))
    
#     # print(states_col_for_county_pop)
#     pop_counties["state"] = states_col_for_county_pop
#     # print(pop_counties)
    
    
    
#     counties_list = []
#     for index, row in pop_counties.iterrows():
#         for state in fips_states_keys:
#             if state in row["Geographic Area"]:
#                 if row["Geographic Area"].find(state) > 1:
#                         counties = row["Geographic Area"].replace(state, '')
#                 if state == "District of Columbia":
#                     # print("trouble maker")
#                     # print(counties)
#                     counties = "District of Columbia"
#         counties_list.append(counties)
#     # for index, row in pop_counties.iterrows():
#     #     if row["state"] in row["Geographic Area"]:
#     #         # print("oh yeah")
#     #         row["Geographic Area"].replace(row["state"], '')
#     #     break
    
#     # print(len(counties_list))
    
    
#     # print((counties_list))
#     pop_counties["Geographic Area"] = counties_list
#     # print(pop_counties)
    
    
#     # for index, row in pop_counties.iterrows():
#     #     if row["Geographic Area"] == "District of Columbia":
#     #         # print("sure") #yes
    
#     # print(specific_date_df)
    
#     for state, state_id in zip(fips_states_keys, fips_states_values):
#         pop_counties["state"] = pop_counties["state"].replace(state, state_id)
     
    
#     specific_date_df["county"] = specific_date_df["county"].str.replace('.', '') # DistrictOfColumbia 
#     pop_counties["Geographic Area"] = pop_counties["Geographic Area"].str.replace('Parish', '') # DistrictOfColumbia
#     pop_counties["Geographic Area"] = pop_counties["Geographic Area"].str.replace(' ', '') # DistrictOfColumbia
    
#     spec_county = list(specific_date_df["county"])
#     spec_state = list(specific_date_df["state"])
#     pop_county = list(pop_counties["Geographic Area"])
#     pop_state = list(pop_counties["state"])
#     population_per_county = list(pop_counties[2019])
    
#     population_counties_list = []
#     # counter = 0
#     for s_county, s_state in zip(spec_county, spec_state): 
#         boo = True
#         for p_county, p_state in zip(pop_county, pop_state):
#             if s_county == p_county and s_state == p_state:
#                 population_counties_list.append(population_per_county[pop_county.index(p_county)]) 
#                 boo = False
#         # counter += 1
#         if boo == True:
#             population_counties_list.append(1) 
#     # print(len(population_counties_list)) # 3065
#     # print(population_counties_list)
#     specific_date_df["county_population"] = population_counties_list
#     # print(specific_date_df)
    
    
#     per100k = []
#     for pop, count in zip(specific_date_df["county_population"], specific_date_df["cases"]):
#         if pop == 1:
#             per100k.append(1)
#         else:
#             per100k.append(100000 * (count/pop))
        
#     specific_date_df["per100k"] = per100k
#     # print(specific_date_df)
#     # print(per100k)
    
#     per10k = []
#     for pop, count in zip(specific_date_df["county_population"], specific_date_df["cases"]):
#         if pop == 1:
#             per10k.append(1)
#         else:
#             per10k.append(10000 * (count/pop))


#     specific_date_df["per10k"] = per10k
#     # print(specific_date_df)
#     # print(per10k)
    
#     # import math
#     log10_per10k = []
#     for item in per10k:
#         # print(item)
#         log10_per10k.append(math.log10(item))
#     specific_date_df["log10_per10k"] = log10_per10k
    
#     # import math
#     log10_per100k = []
#     for item in per100k:
#         # print(item)
#         log10_per100k.append(math.log10(item))
#     specific_date_df["log10_per100k"] = log10_per100k
    
    
#     copy_df = specific_date_df.copy() # this is to remove data from census that is missing from covid
#     copy_df = copy_df[copy_df['log10_per100k'] != 0]
    
#     # Per county geojson
#     with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#         counties = json.load(response)
    
#     # print(counties["features"][0]["properties"]["STATE"])
#     # print((counties["features"][0])) #3221
    
#     # per county
#     fig = px.choropleth(copy_df, geojson=counties,
#                                locations='fips', 
#                                color='log10_per100k',
#                                # color_continuous_scale="Reds",
#                                 color_continuous_scale="Viridis",
#                                range_color=(0, 5),
#                                # locationmode = 'USA-states',
#                                featureidkey = "id",
#                                hover_name = "county",
#                                scope="usa",
#                               )
#     fig.update_layout(margin={"r":5,"t":5,"l":5,"b":5},
#                       title_text = '<br><br>Covid-19 Spread Per 100k Population Per County<br>Using 2019 Census Estimations<br>'+date
#                       )
#     # fig.show()
#     # plot(fig)
#     return fig