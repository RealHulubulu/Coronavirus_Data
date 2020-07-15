# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 09:53:48 2020

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
import numpy as np


# https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv
dfmain = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')

# # local copy
# dfmain = pd.read_csv('time_series_covid19_confirmed_global.csv')

df_pop = pd.read_csv('datasets_547565_1144363_pop_worldometer_data.csv')

# dfpop = pd.read_csv('worldpopcsv.csv')

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
        f.write('\n{% endblock %}')
        
if not os.path.exists("images_global"):
    os.mkdir("images_global")
    
if not os.path.exists("images_global_per100kpop"):
    os.mkdir("images_global_per100kpop")
    
# print(dfmain)

# print(df_pop)
    
# country_from_pop_list = list(df_pop["Country (or dependency)"])
# pop_from_pop_list = list(df_pop["Population (2020)"])

#%%
        
# dates_list = []
dates_list = list(dfmain.keys())
# print(dates_list)
dates_list.remove("Province/State")
dates_list.remove("Country/Region")
dates_list.remove("Lat")
dates_list.remove("Long")
# print(dates_list)





#%%

for date in dates_list:
    

    # date = "7/6/20"
    # date = dates_list[-1]
    
    # date = dates_list[-134]
    
    print(date)
    # print(dfmain)
    
    dup_countries = ["Australia", "Canada", "China", "France", "Netherlands", "United Kingdom"]
    
    
    copy_dfmain = dfmain.copy()
    # print(copy_dfmain.shape)
    
    for dup in dup_countries:
        copy_dfmain = copy_dfmain[copy_dfmain["Country/Region"] != dup] #has none of above dup countries
    
    # print(copy_dfmain.shape)
    
    totals_list = []
    for dup in dup_countries:
        total = 0
        for index, row in dfmain.iterrows():
            if row["Country/Region"] == dup:
                total += row[date]
           
        totals_list.append(total)         
    
    # print(dup_countries)
    # print(totals_list)
    
    
    # country_list_test = list(copy_dfmain["Country/Region"])
    # print(country_list_test)
    
    
    
    
    #%%                 
    # date = "7/6/20"
    
    # print(dfmain.keys())
    
    global_cases_df = pd.DataFrame()
    
    
    country_list = list(copy_dfmain["Country/Region"])
    # country_list.append("Somaliland")
    country_list.append("Greenland")
    # country_list.append("Turkmenistan")
    # country_list.append("North Korea")
    # country_list.append("Antarctica")
    
    for item in dup_countries:
        country_list.append(item)
    
    
    #%%
    # print(country_list)
    #%%
    
    global_cases_df["Country"] = country_list
    
    # print(global_cases_df)
    
    
    # somaliland_cases = 0
    # for index, row in dfmain.iterrows():
    #     if row["Country"] == "Somalia":
    #         somaliland_cases = row["Cases"]
    
    cases_list = list(copy_dfmain[date])
    # cases_list.append(somaliland_cases)
    cases_list.append(0)
    # cases_list.append(0)
    
    for item1 in totals_list:
        cases_list.append(item1)
    
    
    global_cases_df["Total_Cases"] = cases_list
    
    #%%
    # print(list(global_cases_df["Country"])) #266
    
    
    #%%
    # https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson
    
    with urlopen('https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson') as response:
            globe_mapping = json.load(response)
    # print(len(globe_mapping["features"])) #255 total countries
            
    # for i in range(len(globe_mapping["features"])):     
        # print(globe_mapping["features"][i]["properties"]["ADMIN"])
            
    # with open('global.json') as response:
    #         globe_mapping = json.load(response)      
    # print(len(globe_mapping["features"])) #175 
    #%%
    # print(globe_mapping["features"][0])
    
    
    #%%
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Bahamas', 'The Bahamas') #  
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('US', 'United States of America') #  
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Korea, South', 'South Korea') #  
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Serbia', 'Republic of Serbia') #  
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Burma', 'Myanmar') # 
    
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Timor-Leste', 'East Timor') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Tanzania', 'United Republic of Tanzania') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Eswatini', 'Swaziland') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('North Macedonia', 'Macedonia') # 
    
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Czechia', 'Czech Republic') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace("Cote d'Ivoire", 'Ivory Coast') # 
    
    # global_cases_df["Country"] = global_cases_df["Country"].str.replace('Congo (Kinshasa)', 'Democratic Republic of the Congo') # 
    # global_cases_df["Country"] = global_cases_df["Country"].str.replace('Congo (Brazzaville)', 'Republic of Congo') #  
    
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Congo ', '') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('(', '') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace(')', '') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('(Kinshasa)', 'Democratic Republic of the Congo') # 
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('(Brazzaville)', 'Republic of Congo') #  
    
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('Cabo Verde', 'Cape Verde') # 
    
    #%%
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('*', '') #  
    global_cases_df["Country"] = global_cases_df["Country"].str.replace('-', ' ') #  
    
        
    #%%
    overlap = []
    not_overlap = []
            
    for i in range(len(globe_mapping["features"])):
        # print(globe_mapping["features"][i]["properties"]["ADMIN"])
        country_name = globe_mapping["features"][i]["properties"]["ADMIN"]
        
        for c in global_cases_df["Country"]:
            if country_name == c:
                overlap.append(country_name)
                # print(country_name)
            
    # print(states_mapping["features"][0])
            
    # print(overlap)
    # print(len(overlap))
    
    not_overlap = list(set(global_cases_df["Country"]) - set(overlap))
    
    # print(not_overlap)
    
    
    log10_list = []
    for value in cases_list:
        # print(value)
        if value == 0:
            log10_list.append(0)
        else:
            log10_list.append(math.log10(value))
        
    # print(log10_list)
    global_cases_df["log10_scaling"] = log10_list
    
#%%
    
# print(country_from_pop_list)
# print(pop_from_pop_list)
# country_from_pop_list = list(df_pop["Country (or dependency)"])
# pop_from_pop_list = list(df_pop["Population (2020)"])
 
    # overlap_pop_and_country = []
    # not_overlap_pop_and_country = []
    
    # df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('United States', 'United States of America')
    
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace(')', '')
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('(', '')
    
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace(' Czechia', '')
    # df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('North Macedonia', 'Macedonia')
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('St. Vincent & Grenadines', 'Saint Vincent and the Grenadines')
    # df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Congo', 'Republic of Congo')
    
    # df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('DR Republic of Congo', 'Democratic Republic of the Congo')
    
    
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Eswatini', 'Swaziland')
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Cabo Verde', 'Cape Verde')
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Sao Tome & Principe', 'Sao Tome and Principe')
    # df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Tanzania', 'United Republic of Tanzania')
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Guinea-Bissau', 'Guinea Bissau')
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Saint Kitts & Nevis', 'Saint Kitts and Nevis')
    # df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Bahamas', 'The Bahamas')
    # df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Serbia', 'Republic of Serbia')
    df_pop["Country (or dependency)"] = df_pop["Country (or dependency)"].str.replace('Timor-Leste', 'East Timor')
    
    country_from_pop_list = list(df_pop["Country (or dependency)"])

# for country in global_cases_df["Country"]:
#     for country_w_pop in df_pop["Country (or dependency)"]:
#         if country == country_w_pop:
#             overlap_pop_and_country.append(country)
            
# not_overlap_pop_and_country = list(set(global_cases_df["Country"]) - set(overlap_pop_and_country))

# print(overlap_pop_and_country)

# print()

# print(not_overlap_pop_and_country) # ['West Bank and Gaza', 'Diamond Princess', 'Ivory Coast', 'Kosovo', 'MS Zaandam']
    
# print()

# print(country_from_pop_list)

#%%

    pop_from_pop_list = list(df_pop["Population (2020)"])
    # sorted_pop_from_pop_list = sorted(pop_from_pop_list)
    
    # print(country_from_pop_list)
    
    
    # print(df_pop["Country (or dependency)"])
    # print()
    
    # print(global_cases_df["Country"])
    # print()
    
    # sorted_country_from_pop_list = sorted(country_from_pop_list)
    
    
    covid_cases_list_for_pop_df = []
    covid_country_list_for_pop_df = []
    covid_pop_list_for_pop_df = []
    
    for index, row in global_cases_df.iterrows():
        for c, p in zip(country_from_pop_list, pop_from_pop_list):
        # print(c)
        # for index, row in global_cases_df.iterrows():
            if c == row["Country"]:
                covid_cases_list_for_pop_df.append(row["Total_Cases"])
                covid_country_list_for_pop_df.append(c)
                covid_pop_list_for_pop_df.append(p)
                
    # print(covid_cases_list_for_pop_df)
    # print(len(covid_cases_list_for_pop_df))
    # print(len(covid_country_list_for_pop_df))
    # print(len(covid_pop_list_for_pop_df))
    
    cases_per_pop_list  = []
    
    for cases, pop in zip(covid_cases_list_for_pop_df, covid_pop_list_for_pop_df):
        cases_per_pop_list.append(cases/pop)
        
    cases_per_pop_list_per_100k = []
    
    for thing in cases_per_pop_list:
        cases_per_pop_list_per_100k.append(thing * 100000)
        
    log10_per_100k = []
    for thing in cases_per_pop_list_per_100k:
        if thing == 0:
            log10_per_100k.append(0)
        else:
            log10_per_100k.append(math.log10(thing))
    
    
    # log10_list_pop_cases = []
    # for value in cases_per_pop_list:
    #     # print(value)
    #     if value == 0:
    #         log10_list_pop_cases.append(0)
    #     else:
    #         log10_list_pop_cases.append(math.log10(value))
        
    # print(log10_list)
    # df_pop["log10_scaling"] = log10_list_pop
    
    
    cases_pop_country_df = pd.DataFrame()
    cases_pop_country_df["Country"] = covid_country_list_for_pop_df
    cases_pop_country_df["Cases"] = covid_cases_list_for_pop_df
    cases_pop_country_df["Pop"] = covid_pop_list_for_pop_df
    
    cases_pop_country_df["Cases_per_Pop"] = cases_per_pop_list
    
    cases_pop_country_df["Cases_per_100k_Pop"] = cases_per_pop_list_per_100k
    
    cases_pop_country_df["Log10_Cases_per_100k_Pop"] = log10_per_100k
    
    
    # print(cases_pop_country_df)
    # print(cases_pop_country_df.shape)
    
    # print()
    
    # print(max(cases_per_pop_list))
    # print(max(cases_per_pop_list_per_100k))
    # print(max(log10_per_100k))

#%%

    fig = px.choropleth(cases_pop_country_df, geojson=globe_mapping,
                                        locations='Country', 
                                        color='Log10_Cases_per_100k_Pop',
                                        # color_continuous_scale="Viridis_r",
                                        # color_continuous_scale="tropic",
                                        color_continuous_scale=[[0.0,'rgb(0,0,250)'],
                                                                [0.2,'rgb(43,140,200)'],
                                                                [0.4, 'rgb(149,207,216)'],
                                                                [0.5, 'rgb(234,252,258)'],
                                                                [0.6, 'rgb(255,210,0)'],
                                                                [0.8, 'rgb(200,0,0)'],
                                                                [1.0, 'rgb(18,5,5)']],
                                        range_color=(0, 5), # for log10
                                        # range_color=(0, 4000000),
        
                                        # locationmode = 'USA-states',
                                        featureidkey = "properties.ADMIN",
                                        hover_name = "Country",
                                        hover_data = ["Cases", "Pop", "Cases_per_Pop", "Cases_per_100k_Pop", "Log10_Cases_per_100k_Pop"],
                                        
                                        scope="world",
                                        labels={'Log10_Cases_per_100k_Pop':'log10(cases/10k)'}
                                      )
    fig.update_layout(margin={"r":5,"t":20,"l":5,"b":5},
                              title_text = '<br><br>Covid-19 log10(cases/100k)<br>'+date,
                                titlefont = {"size": 30, "color":"White"},
                                 paper_bgcolor='#4E5D6C',
                                 plot_bgcolor='#4E5D6C',
                                 geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C', landcolor='rgba(51,17,0,0.2)'),
                                 font = {"size": 14, "color":"White"},
                                autosize = False,
                                width = 1500,
                                height = 1000
                                
                              )
        
    # plot(fig)
    
    reformatted_date = date.replace("/", "-")
    
    fig.write_image("C:/Users/karas/.spyder-py3/coronavirus/images_global_per100kpop/"+reformatted_date+"_global_per100kpop.png")
    # break
    
    # plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_rt.html')


    # # below is how it writes current html and png
    # fig.write_image("C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/pages/static/current_global_cases_map_per100kpop.png")
    # plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_globe_per100kpop.html')
        
    # html_header = """
    # {% extends 'base.html' %}
    # {% block content %}
    # <body style="background-color:black;color:white;">
    #     """
    # line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_globe_per100kpop.html', html_header)
        
    
    
    # line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_rt.html', html_header)    

    # break


    
    
    
    #%%
    # # total cases
    # fig = px.choropleth(global_cases_df, geojson=globe_mapping,
    #                                 locations='Country', 
    #                                 color='log10_scaling',
    #                                 # color_continuous_scale="Viridis_r",
    #                                 # color_continuous_scale="tropic",
    #                                 color_continuous_scale=[[0.0,'rgb(0,0,250)'],
    #                                                         [0.2,'rgb(43,140,200)'],
    #                                                         [0.4, 'rgb(149,207,216)'],
    #                                                         [0.5, 'rgb(234,252,258)'],
    #                                                         [0.6, 'rgb(255,210,0)'],
    #                                                         [0.8, 'rgb(200,0,0)'],
    #                                                         [1.0, 'rgb(18,5,5)']],
    #                                 range_color=(0, 9), # for log10
    #                                 # range_color=(0, 4000000),
    
    #                                 # locationmode = 'USA-states',
    #                                 featureidkey = "properties.ADMIN",
    #                                 hover_name = "Country",
    #                                 hover_data = ["log10_scaling",                                        
    #                                               "Total_Cases"],
                                    
    #                                 scope="world",
    #                                 labels={'log10_scaling':'log(total cases)'}
    #                               )
    # fig.update_layout(margin={"r":5,"t":20,"l":5,"b":5},
    #                       title_text = '<br><br>Covid-19 total cases per country<br>'+date,
    #                         titlefont = {"size": 30, "color":"White"},
    #                          paper_bgcolor='#4E5D6C',
    #                          plot_bgcolor='#4E5D6C',
    #                          geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C', landcolor='rgba(51,17,0,0.2)'),
    #                          font = {"size": 14, "color":"White"},
    #                         autosize = False,
    #                         width = 1500,
    #                         height = 1000
                            
    #                       )
    
    # # plot(fig)
    
    # reformatted_date = date.replace("/", "-")
    
    # # fig.write_image("C:/Users/karas/.spyder-py3/coronavirus/images_global/"+reformatted_date+"_global.png")
    # # break
           

    # fig.write_image("C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/pages/static/current_global_cases_map.png")
    # plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_globe.html')
            
    # # plot(fig,filename='C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_rt.html')
    
        
    # html_header = """
    # {% extends 'base.html' %}
    # {% block content %}
    # <body style="background-color:black;color:white;">
    #     """
    # line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/Current_globe.html', html_header)
        
    # # line_prepender('C:/Users/karas/.spyder-py3/Covid_Maps_Heroku/main_site_covid/templates/'+new_date+'_rt.html', html_header)    

    # break
    
    
#%%
    
    # for total cases
    
# from PIL import Image, ImageDraw
# import PIL
# import os
# images = []
# directory = 'C:/Users/karas/.spyder-py3/coronavirus/images_global'
# for filename in os.listdir(directory):
#     # print("hi")
#     f = Image.open('C:/Users/karas/.spyder-py3/coronavirus/images_global/'+filename)
#     # f = f.save(filename)
#     images.append(f)

# print(len(images))   
# images[0].save('covid_timeline_global_total_cases.gif',
#                 save_all=True, append_images=images[1:], optimize=False, duration=600, loop=0)
    
#%%
    
    # for cases per 100k
    
# from PIL import Image, ImageDraw
# import PIL
# import os
# images = []
# directory = 'C:/Users/karas/.spyder-py3/coronavirus/images_global_per100kpop'
# for filename in os.listdir(directory):
#     # print("hi")
#     f = Image.open('C:/Users/karas/.spyder-py3/coronavirus/images_global_per100kpop/'+filename)
#     # f = f.save(filename)
#     images.append(f)

# print(len(images))   
# images[0].save('covid_timeline_global_cases_per100kpop.gif',
#                 save_all=True, append_images=images[1:], optimize=False, duration=600, loop=0)

