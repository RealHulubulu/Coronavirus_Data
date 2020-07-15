# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 08:53:42 2020

@author: karas
"""

from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import plotly
from plotly.offline import plot
import os
import math

#this auto downloads most recent rt.csv
import requests
url = 'https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv'
r = requests.get(url, allow_redirects=True)
open('rt.csv', 'wb').write(r.content)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

#%%

if not os.path.exists("images_perCap"):
    os.mkdir("images_perCap")

if not os.path.exists("images_rt"):
    os.mkdir("images_rt")
    

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
        f.write('\n{% endblock %}')

#%%
my_file = os.path.join(THIS_FOLDER, 'rt.csv')
rt_df = pd.read_csv(open(my_file))

# print(rt_df)

with urlopen('https://gist.githubusercontent.com/wavded/1250983/raw/bf7c1c08f7b1596ca10822baeb8049d7350b0a4b/stateCodeToFips.json') as response:
    fips_states_abrev = json.load(response)
fips_states_abrev_keys = list(fips_states_abrev.keys())
fips_states_abrev_values = list(fips_states_abrev.values())



#%%
dates_list = list(rt_df["date"].unique())
# print(len(dates_list))
dates_list = sorted(dates_list)
# print(dates_list)
# print(dates_list.index("2020-03-08")) # 49

# dates_list = dates_list[49:] # this does it from when all states had it

current_date = dates_list[0]

# print()
# print(dates_list)

for new_date in dates_list:

    states_fips_rt_df = pd.DataFrame()
    single_date_states = []
    single_date_rt = []
    
    single_date_state_name = []
    single_date_positive = []
    single_date_tests = []
    single_date_new_tests = []
    single_date_new_cases = []
    single_date_new_deaths = []
    
    new_date = dates_list[-1] # use if capturing final day
    # new_date = "2020-07-03"
    print("Date: ", new_date)
    
    for index, row in rt_df.iterrows():
        if row["date"] == new_date:
            single_date_states.append(row["region"])
            single_date_rt.append(row["mean"])
            
            single_date_state_name.append(row["region"])
            single_date_positive.append(row["positive"])
            single_date_tests.append(row["tests"])
            single_date_new_tests.append(row["new_tests"])
            single_date_new_cases.append(row["new_cases"])
            single_date_new_deaths.append(row["new_deaths"])
    
    states_fips_rt_df["state_fips"] = single_date_states
    states_fips_rt_df["rt_mean"] = single_date_rt
    
    states_fips_rt_df["region"] = single_date_state_name
    states_fips_rt_df["positive"] = single_date_positive 
    states_fips_rt_df["tests"] = single_date_tests
    states_fips_rt_df["new_tests"] = single_date_new_tests
    states_fips_rt_df["new_cases"] = single_date_new_cases
    states_fips_rt_df["new_deaths"] = single_date_new_deaths
    
    single_date_percent_positive = []
    percent = 0
    for cases, tests in zip(single_date_new_cases,single_date_new_tests):
        if tests == 0:
            percent == 0
        else:
            percent = cases/tests
        single_date_percent_positive.append(percent)
    states_fips_rt_df["percent_positive"] = single_date_percent_positive
       
    
    
    for state, state_id in zip(fips_states_abrev_keys, fips_states_abrev_values):
        states_fips_rt_df['state_fips'] = states_fips_rt_df['state_fips'].replace(state, state_id)
        
        
    #%%
    
    # for doing state per capita ( new cases / population )
    
    my_file = os.path.join(THIS_FOLDER, 'population_states_2019.txt')
    pop_states = pd.read_csv(my_file, header=0)
    
    
    with urlopen('https://gist.githubusercontent.com/wavded/1250983/raw/bf7c1c08f7b1596ca10822baeb8049d7350b0a4b/stateToFips.json') as response:
        fips_states = json.load(response)       
    fips_states_keys = list(fips_states.keys())
    fips_states_values = list(fips_states.values())
    fips_states_keys = [w.replace('ogia', 'orgia') for w in fips_states_keys]
    
    for state, state_id in zip(fips_states_keys, fips_states_values):
        pop_states['State'] = pop_states['State'].replace(state, state_id)
    
    # print(type(pop_states["State"][0])) #str
    
    pop_list = []
    for state in states_fips_rt_df["state_fips"]:
        for i,row in pop_states.iterrows():
            if row["State"] == state:
                pop_list.append(row["Population"])
     
    # print(len(pop_list)) #0        
    states_fips_rt_df["state_pop"] = pop_list

# print(states_fips_rt_df)
# print()
# print(pop_list)
# print()
# print(pop_states)
    per_cap_list = []
    per_capita_per100k = []
    for cases, pop in zip(single_date_new_cases, pop_list):
        per_capita = cases/pop
        per_cap_list.append(per_capita)
        per_capita_per100k.append(100000 * per_capita)
    states_fips_rt_df["per_capita"] = per_cap_list
    
    states_fips_rt_df["per_capita_per_100k"] = per_capita_per100k
    
    # print(max(per_capita_per100k))
    
    
    #%%
    

    with open('gz_2010_us_040_00_20m.json') as response:
        states_mapping = json.load(response)
      
    # print(states_mapping["features"][0]["properties"]["STATE"])
    # print(states_mapping["features"][0]) #3221
#%%
        
#     # per state
#     fig = px.choropleth(states_fips_rt_df, geojson=states_mapping,
#                                 locations='state_fips', 
#                                 color='rt_mean',
#                                 # color_continuous_scale="icefire",
#                                 # color_continuous_scale="tropic",
#                                 color_continuous_scale=[[0.0,'rgb(0,0,250)'],
#                                                         [0.2,'rgb(43,140,200)'],
#                                                         [0.4, 'rgb(149,207,216)'],
#                                                         [0.5, 'rgb(234,252,258)'],
#                                                         [0.6, 'rgb(255,210,0)'],
#                                                         [0.8, 'rgb(200,0,0)'],
#                                                         [1.0, 'rgb(18,5,5)']],
#                                 # range_color=(0, 4),
#                                 range_color=(0, 2),

#                                 # locationmode = 'USA-states',
#                                 featureidkey = "properties.STATE",
#                                 hover_name = "region",
#                                 hover_data = ["rt_mean",                                            
#                                               "new_tests",
#                                               "new_cases",
#                                               "percent_positive",
#                                               "new_deaths"],
#                                 scope="usa",
#                                 labels={'rt_mean':'Rt mean'}
#                               )
#     fig.update_layout(margin={"r":5,"t":20,"l":5,"b":5},
#                       title_text = '<br><br>Covid-19 Rt Mean Per State Using rt.live <br>'+ new_date,
#                       titlefont = {"size": 15, "color":"White"},
#                         paper_bgcolor='#4E5D6C',
#                         plot_bgcolor='#4E5D6C',
#                         geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
#                         font = {"size": 14, "color":"White"},
#                         autosize = False,
#                         width = 800,
#                         height = 650
                        
#                       )
#     # fig.show()
#     # plot(fig,filename='covid_Rt_'+new_date+'.html')
#     # plot(fig)
#     fig.write_image("images_rt/"+new_date+"_rt_per_state.png")
    
#     # break
    
#     # plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_rt.html')
    
    
#     fig.write_image("C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/pages/static/current_rt_per_state.png")
#     plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_rt.html')
    
#     html_header = """
# {% extends 'base.html' %}
# {% block content %}
# <body style="background-color:black;color:white;">
#     """
#     line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_rt.html', html_header)
    
    
    
#     # line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_rt.html', html_header)    
    
#     break
    

#%%
    # per capita
    fig = px.choropleth(states_fips_rt_df, geojson=states_mapping,
                                locations='state_fips', 
                                color='per_capita_per_100k',
                                # color_continuous_scale="icefire",
                                # color_continuous_scale="tropic",
                                color_continuous_scale=[[0.0,'rgb(0,0,250)'],
                                                        [0.2,'rgb(43,140,200)'],
                                                        [0.4, 'rgb(149,207,216)'],
                                                        [0.5, 'rgb(234,252,258)'],
                                                        [0.6, 'rgb(255,210,0)'],
                                                        [0.8, 'rgb(200,0,0)'],
                                                        [1.0, 'rgb(18,5,5)']],
                                # range_color=(0, 4),
                                range_color=(0, 80),

                                # locationmode = 'USA-states',
                                featureidkey = "properties.STATE",
                                hover_name = "region",
                                hover_data = ["per_capita_per_100k",
                                              "per_capita",                                            
                                              "new_tests",
                                              "new_cases",
                                              "percent_positive",
                                              "new_deaths"],
                                scope="usa",
                                labels={'per_capita_per_100k':'PC/100k'},
                                
                              )
    fig.update_layout(margin={"r":5,"t":20,"l":5,"b":5},
                      title_text = '<br><br>Covid-19 Per Capita Per 100k Population <br>'+ new_date,
                        titlefont = {"size": 15, "color":"White"},
                        paper_bgcolor='#4E5D6C',
                        plot_bgcolor='#4E5D6C',
                        geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                        font = {"size": 14, "color":"White"},
                        autosize = False,
                        width = 800,
                        height = 650
                      )
    
    
    # fig.show()
    # plot(fig,filename='covid_Rt_'+new_date+'.html')
    # plot(fig)
    # fig.write_image("images_perCap/"+new_date+"_PC_per_state.png")
    
    # break
    
    # plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_perCap.html')
    
    
    fig.write_image("C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/pages/static/current_perCap_per_state.png")
    plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_perCap.html')

    html_header = """
{% extends 'base.html' %}
{% block content %}
<body style="background-color:black;color:white;">
    """
    line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_perCap.html', html_header)
    
    
    # line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_perCap.html', html_header)

    break




#%%
# from PIL import Image, ImageDraw
# import PIL
# import os
# images = []

# # directory = 'C:/Users/karas/.spyder-py3/coronavirus/images_rt'
# directory = 'C:/Users/karas/.spyder-py3/coronavirus/images_perCap'

# for filename in os.listdir(directory):
#     # print("hi")
#     # f = Image.open('C:/Users/karas/.spyder-py3/coronavirus/images_rt/'+filename)
#     f = Image.open('C:/Users/karas/.spyder-py3/coronavirus/images_perCap/'+filename)
#     # f = f.save(filename)
#     images.append(f)

# print(len(images))   
# # images[0].save('covid_timeline_rt_centered1.gif',
# images[0].save('covid_timeline_perCap.gif',
#                 save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

