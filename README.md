# Coronavirus_Data

This is some code that uses plotly to visualize covid in the US on 6/28/2020. The data that has been used by the New York Times was published to kaggle. The data 
has case counts and death counts per county since January of 2020 up until 6/28/2020 (as of writing this). The code makes a heat map. The current code published 
creates a heat map per 100k population. It is easy to see how to adjust the input for plotly to get other heat maps.

Covid dataset on kaggle: https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset

Where I got my geojson: https://eric.clst.org/tech/usgeojson/

## Heat Maps


This is the data per state total count.

![Per State Total Count](/covid_total_states.png)

This is the data per 100k population per state.

![Per State Total Count](/covid_per100k_states.png)
