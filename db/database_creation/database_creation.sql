
-- intake database
\c postgres; 
SELECT 'CREATE DATABASE bronze'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bronze')\gexec
-- connect
\c bronze;

-- create the tables

-- covid_19_daily_cases    :    daily covid data, no geographic data
CREATE TABLE IF NOT EXISTS covid_19_daily_cases(
    lab_report_date         date PRIMARY KEY,
    cases_total             int,
    deaths_total            int,
    hospitalizations_total  int
    );

-- covid_19_zip    :    weekly covid incidence data by zip code
CREATE TABLE IF NOT EXISTS covid_19_zip(
    row_id                  VARCHAR(15) PRIMARY KEY, -- auto incrementing primary key
    zip_code                varchar(8), -- zip code
    week_number             int, -- week number, beginning 2020. see CDC MMWR weeks
    week_start              date, -- beginning of the week
    cases_weekly            int,  -- empty if less than 5
    case_rate_cumulative    float,    -- weekly rate per 100k
    deaths_weekly           int,     -- weekly deaths
    death_rate_weekly       float    -- deaths per 100k
    );

-- taxi_trips    :    list of taxi trips, with start and end points
CREATE TABLE IF NOT EXISTS taxi_trips(
    trip_id                     varchar(50) PRIMARY KEY, -- trip id hash 
    taxi_id                     varchar(128), -- taxi id hash
    trip_start_timestamp        date, -- start of trip
    trip_seconds                int, -- trip length in seconds
    trip_miles                  float, -- not very useful, since this is really based off census tracts...
    pickup_centroid_latitude    float, -- latitude of pickup location
    pickup_centroid_longitude   float, -- longitude of pickup location
    dropoff_centroid_latitude   float, -- latitude of dropoff location
    dropoff_centroid_longitude  float, -- longitude of dropoff location
    pickup_community_area       int, -- community area number of the pickup location. Blank outside Chicago
    dropoff_community_area      int -- community area number of the dropoff location. Blank outside Chicago
);


-- TNP_trips    :    list of rideshare trips, with start and end points
CREATE TABLE IF NOT EXISTS tnp_trips(
    trip_id                     VARCHAR(50) PRIMARY KEY, -- trip id hash 
    trip_seconds                int,
    trip_start_timestamp        date,    -- trip length in seconds
    trip_miles                  float,    -- not very useful, since this is really based off census tracts...
    pickup_community_area       int,    -- community area number. blank outside chicago
    dropoff_community_area      int,    -- community area number. blank outside chicago
    pickup_centroid_latitude    float,    -- latitude of pickup location
    pickup_centroid_longitude   float,    -- longitude of pickup location
    dropoff_centroid_latitude   float,    -- latitude of dropoff location
    dropoff_centroid_longitude  float    -- longitude of dropoff location
);


-- build_permit    :    list of building permits
CREATE TABLE IF NOT EXISTS  build_permit(
    id                          int PRIMARY KEY, -- building permit id
    permit_                     int,  -- number assigned at beginning of application process
    permit_type                 varchar(35), -- type of permit
    application_start_date      date, -- start of application date
    issue_date                  date, -- date it was issued
    community_area              int,  -- community area number
    ward                        int,  -- I would argue this is more important that community area
    latitude                    float, -- latitude of the building
    longitude                   float -- longitude of the building
);


-- health_ind :    table of health and other community indicators
CREATE TABLE IF NOT EXISTS health_ind(
    community_area              int PRIMARY KEY, -- this doesn't match the other info!
    community_area_name         varchar(100), -- community area name
    below_poverty_level         float, -- percent of households in below poverty level
    no_high_school_diploma      float, -- percent persons >25yo
    per_capita_income           float, -- dollars
    unemployment                float  -- percent of persons >16yo
);

-- database for transformed datasets
SELECT 'CREATE DATABASE silver'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'silver')\gexec
\c silver;

-- taxi/rideshare enum
CREATE TYPE ride_types AS ENUM ('taxi','rideshare');

-- requirement 1: covid in zip codes vs taxis
CREATE TABLE IF NOT EXISTS taxi_covid(
    ind                         SERIAL PRIMARY KEY, -- primary key
    ride_type                   ride_types, -- taxi or rideshare?
    ride_date                   date, -- date of the rides
    zip_start                   int,  -- pick up zip code
    zip_end                     int,  -- destination zip code
    covid_rate                  float, -- weekly covid rate (that's all we've got...)
    num_rides                   int -- number of rides to that zip
);

-- requirement 2 -- taxis from airports to zip codes vs covid rates
--             I think this is just a subset of above...
-- for midway
CREATE TABLE IF NOT EXISTS midway_taxi_covid(
    ind                     SERIAL PRIMARY KEY, -- primary key
    ride_type               ride_types, -- taxi or rideshare?
    ride_date               date, -- date of the rides
    zip                     int,  -- destination zip code
    covid_rate              float, -- weekly covid rate (that's all we've got...)
    num_rides               int -- number of rides to that zip
);
-- for o'hare
CREATE TABLE IF NOT EXISTS ohare_taxi_covid(
    ind                     SERIAL PRIMARY KEY, -- primary key
    ride_type               ride_types, -- taxi or rideshare?
    ride_date               date, -- date of the rides
    zip                     int,  -- destination zip code
    covid_rate              float, -- weekly covid rate (that's all we've got...)
    num_rides               int -- number of rides to that zip
);

-- requirement 3 -- taxi trip #s vs covid vulnerability index
CREATE TABLE IF NOT EXISTS ccvi_taxi(
    trip_id                 varchar(50) PRIMARY KEY, -- trip number
    taxi_id                 varchar(100), -- taxi number; may be NULL if it's ride share
    ride_type               ride_types, -- taxi or rideshare?
    comm_area_start         varchar(100),
    comm_area_end           varchar(100)
);

-- requirement 5 -- building permits by neighborhood with unemployment, poverty, income info
CREATE TABLE IF NOT EXISTS permit_neighborhood(
    permit_id               int PRIMARY KEY, -- building permit id
    neighborhood            varchar(100), -- neighborhood name
    unemployment            float, -- perc over 16yo
    poverty                 float, -- per households
    income                  float
);

-- req 6 -- building permits by zip code, with health measures
CREATE TABLE IF NOT EXISTS permit_zip(
    permit_id               int PRIMARY KEY, -- building permit id
    zip                     int, -- zip code
    unemployment            float, -- perc over 16yo
    poverty                 float, -- per households
    income                  float
);

-- taxi counts (start with just date)
--         we'll split it by type so that we can compare those. Seems interesting
CREATE TABLE IF NOT EXISTS taxi_count(
    id                      SERIAL PRIMARY KEY, -- primary key
    date                    date, 
    zip                     int,
    taxi_count              int,
    rideshare_count         int
);



-- database for output data
SELECT 'CREATE DATABASE gold'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'gold')\gexec

\c gold;

