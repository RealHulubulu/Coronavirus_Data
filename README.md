# Coronavirus_Data

This is some code that uses plotly to visualize covid in the US. The data that has been used by the New York Times was published to kaggle. The data 
has case counts and death counts per county since January of 2020 up until yesterday (yep, yesterday). The code makes a heat map. The current code published 
creates a heat map per 100k population. It is easy to see how to adjust the input for plotly to get other heat maps.

Covid dataset on kaggle: https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset

Where I got my state geojson: https://eric.clst.org/tech/usgeojson/

Where I got my county geojson (and also a nifty tutorial on making this graphs): https://plotly.com/python/choropleth-maps/

Where I got my 2019 census data. It's the United States one: https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/

Link to the Rt data and live dashboards: https://rt.live/

## Covid Cases Heat Maps
Link to time-lapses of all maps hosted on my website. These gifs can also be found in this repo.

http://www.visualizecovid19.live/gifs/

This is the data per 100k population per county on 6/29/2020

![Per County Total Count per 100k](/covid_per100k_counties_06292020.png)

### Rt Heat Maps

This is the Rt data per state for 3/08/2020.

![Per State rt](/2020-03-08_rt_per_state.png)

This is the Rt data per state for 3/28/2020.

![Per State rt](/2020-03-28_rt_per_state.png)

This is the Rt data per state for 5/14/2020.

![Per State rt](/2020-05-14_rt_per_state.png)

This is the Rt data per state for 6/29/2020.

![Per State rt](/2020-06-29_rt_per_state.png)



