# Coronavirus_Data

This is some code that uses plotly to visualize covid in the US on 6/28/2020. The data that has been used by the New York Times was published to kaggle. The data 
has case counts and death counts per county since January of 2020 up until 6/28/2020 (as of writing this). The code makes a heat map. The current code published 
creates a heat map per 100k population. It is easy to see how to adjust the input for plotly to get other heat maps.

Covid dataset on kaggle: https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset

Where I got my state geojson: https://eric.clst.org/tech/usgeojson/

Where I got my county geojson (and also a nifty tutorial on making this graphs): https://plotly.com/python/choropleth-maps/

Where I got my 2019 census data. It's the United States one: https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html

## Heat Maps
Link to a time lapse of county total cases per 100k population from 1/21/2020 to 6/29/2020. There are some gaps in the map because the census data doesn't work well with the covid data. I am working to fix this.

https://imgur.com/gallery/NfTeIyF

This is the data per state total count.

![Per State Total Count](/covid_total_states_06282020.png)

This is the data per 100k population per state.

![Per State Total Count](/covid_per100k_states_06282020.png)

This is the data per 100k population per county. There are gaps where the census data isn't matching up well. I am working to fix it.

![Per State Total Count](/covid_per100k_counties_06292020.png)


