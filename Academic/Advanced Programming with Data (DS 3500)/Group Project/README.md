# Weather-Witches-project

Luna Correia & Maverick Donald-Wright

## How to run the data pipeline
- Create a `.env` file and add your OpenAQ API key 
to it with the variable name 'OPENAQ_KEY'
- Run `process_data.py`, which calls all the pipeline functions in order


## Data cleaning decisions
- We used inner joins when merging the air quality, weather, and park location data
- 

## Known data quality issues 
- There isn't a "size" value for the national parks that I'm aware of,
so I chose the 10km radius to search for sensors sort of arbitrarily. Limiting
this range in some way is necessary, but it does mean that some parks won't get
air quality data, so will have to end up dropped
- Different air quality sensors measure different things, so that needs to be dealt
with in regard to using any of them for the air quality metric 
  - *could pick just one attribute that has the most readings to use*
