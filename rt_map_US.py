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

if not os.path.exists("images_rt"):
    os.mkdir("images_rt")
    

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


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
dates_list = dates_list[49:]
current_date = dates_list[0]

# print()
# print(dates_list)

for new_date in dates_list:

    states_fips_rt_df = pd.DataFrame()
    single_date_states = []
    single_date_rt = []
    
    for index, row in rt_df.iterrows():
        if row["date"] == new_date:
            single_date_states.append(row["region"])
            single_date_rt.append(row["mean"])
    
    
    states_fips_rt_df["state"] = single_date_states
    states_fips_rt_df["rt_mean"] = single_date_rt
    
    
    for state, state_id in zip(fips_states_abrev_keys, fips_states_abrev_values):
        states_fips_rt_df['state'] = states_fips_rt_df['state'].replace(state, state_id)
    

    with open('gz_2010_us_040_00_20m.json') as response:
        states_mapping = json.load(response)
      
    # print(states_mapping["features"][0]["properties"]["STATE"])
    # print(states_mapping["features"][0]) #3221
    #%%
    # per state
    fig = px.choropleth(states_fips_rt_df, geojson=states_mapping,
                                locations='state', 
                                color='rt_mean',
                                color_continuous_scale="icefire",
                                range_color=(0, 4),
                                # locationmode = 'USA-states',
                                featureidkey = "properties.STATE",
                                hover_name = "state",
                                scope="usa",
                                labels={'rt_mean':'Rt mean'}
                              )
    fig.update_layout(margin={"r":5,"t":5,"l":5,"b":5},
                      title_text = '<br><br>Covid-19 Rt Mean Per State Using rt.live <br>'+ new_date
                      )
    # fig.show()
    # plot(fig)
    fig.write_image("images_rt/"+new_date+"_rt_per_state.png")
    # break
    




#%%
# from PIL import Image, ImageDraw
# import PIL
# import os
# images = []
# directory = 'C:/Users/karas/.spyder-py3/coronavirus/images_rt'
# for filename in os.listdir(directory):
#     # print("hi")
#     f = Image.open('C:/Users/karas/.spyder-py3/coronavirus/images_rt/'+filename)
#     # f = f.save(filename)
#     images.append(f)

# print(len(images))   
# #%%
# images[0].save('covid_timeline_rt.gif',
#                 save_all=True, append_images=images[1:], optimize=False, duration=400, loop=0)

