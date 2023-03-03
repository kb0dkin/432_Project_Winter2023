-- new enumeration types

-- taxi/rideshare enum
CREATE TYPE ride_types AS ENUM ('taxi','rideshare')



-- intake database
\c default -- connect to the "pg" admin database
SELECT 'CREATE DATABASE bronze'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bronze')\gexec
-- connect
\c bronze;

-- create the tables

-- covid_19_daily_cases	:	daily covid data, no geographic data
CREATE TABLE IF NOT EXISTS covid_19_daily_cases(
	date_rec		date PRIMARY KEY,
	cases			int,
	deaths			int,
	hospitalizations	int
	);

-- covid_19_zip	:	weekly covid incidence data by zip code
CREATE TABLE IF NOT EXISTS covid_19_zip(
	id				SERIAL PRIMARY KEY, -- auto incrementing primary key
	zip				varchar(5), -- zip code
	week_num		int, -- week number, beginning 2020. see CDC MMWR weeks
	week_start		date, -- beginning of the week
	cases_week		int,  -- empty if less than 5
	case_rate		float,	-- weekly rate per 100k
	death_week		int, 	-- weekly deaths
	death_rate		float	-- deaths per 100k
);

-- taxi_trips	:	list of taxi trips, with start and end points
CREATE TABLE IF NOT EXISTS taxi_trips(
	trip_id				varchar(50) PRIMARY KEY, -- trip id hash 
	taxi_id				varchar(128), -- taxi id hash
	trip_len			int,	-- trip length in seconds
	trip_dist			float,	-- not very useful, since this is really based off census tracts...
	comm_area_start		int,	-- community area number. blank outside chicago
	lat_long_start		geography(point), --
	comm_area_end		int		-- community area number. blank outside chicago
)


-- TNP_trips	:	list of rideshare trips, with start and end points
CREATE TABLE IF NOT EXISTS TNP_trips(
	trip_id				varchar(50) PRIMARY KEY, -- trip id hash 
	trip_len			int,	-- trip length in seconds
	trip_dist			float,	-- not very useful, since this is really based off census tracts...
	comm_area_start		int,	-- community area number. blank outside chicago
	comm_area_end		int		-- community area number. blank outside chicago
)

-- build_permit	:	list of building permits
CREATE TABLE IF NOT EXISTS  build_permit(
	permit_id			int PRIMARY KEY, -- building permit id
	permit_num			int,  -- number assigned at beginning of application process
	app_start_date		date, -- start of application date
	issue_date			date, -- date it was issued
	comm_area			int,  -- community area number
	ward				int,  -- I would argue this is more important that community area
	location			geography(POINT) -- point in WGS84
)


-- health_ind :	table of health and other community indicators
CREATE TABLE IF NOT EXISTS health_ind(
	comm_num			int PRIMARY KEY, -- this doesn't match the other info!
	comm_name			varchar(100), -- community area name
	pov_rate			float, -- percent of households in below poverty level
	no_hs_grad			float, -- percent persons >25yo
	income				float, -- dollars
	unemployment		float  -- percent of persons >16yo
);


-- database for transformed datasets
SELECT 'CREATE DATABASE silver'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'silver')\gexec
\c silver;

-- requirement 1: covid in zip codes vs taxis
CREATE TABLE IF NOT EXISTS taxi_covid(
	ind					SERIAL PRIMARY KEY, -- primary key
	ride_type			ride_types, -- taxi or rideshare?
	ride_date			date, -- date of the rides
	zip_start			int,  -- pick up zip code
	zip_end				int,  -- destination zip code
	covid_rate			float, -- weekly covid rate (that's all we've got...)
	num_rides			int -- number of rides to that zip
)

-- requirement 2 -- taxis from airports to zip codes vs covid rates
-- 			I think this is just a subset of above...
-- for midway
CREATE TABLE IF NOT EXISTS midway_taxi_covid(
	ind					SERIAL PRIMARY KEY, -- primary key
	ride_type			ride_types, -- taxi or rideshare?
	ride_date			date, -- date of the rides
	zip					int,  -- destination zip code
	covid_rate			float, -- weekly covid rate (that's all we've got...)
	num_rides			int -- number of rides to that zip
)
-- for o'hare
CREATE TABLE IF NOT EXISTS ohare_taxi_covid(
	ind					SERIAL PRIMARY KEY, -- primary key
	ride_type			ride_types, -- taxi or rideshare?
	ride_date			date, -- date of the rides
	zip					int,  -- destination zip code
	covid_rate			float, -- weekly covid rate (that's all we've got...)
	num_rides			int -- number of rides to that zip
)


-- requirement 3 -- taxi trip #s vs covid vulnerability index
CREATE TABLE IF NOT EXISTS ccvi_taxi(
	trip_id				varchar(50) PRIMARY KEY, -- trip number
	taxi_id				varchar(100), -- taxi number; may be NULL if it's ride share
	ride_type			ride_types, -- taxi or rideshare?
	comm_area_start		varchar(100),
	comm_area_end		varchar(100)

)


-- requirement 5 -- building permits by neighborhood with unemployment, poverty, income info
CREATE TABLE IF NOT EXISTS permit_neighborhood(
	permit_id			int PRIMARY KEY, -- building permit id
	neighborhood 		varchar(100), -- neighborhood name
	unemployment		float, -- perc over 16yo
	poverty				float, -- per households
	income				float
)

-- req 6 -- building permits by zip code, with health measures
CREATE TABLE IF NOT EXISTS permit_zip(
	permit_id			int PRIMARY KEY, -- building permit id
	zip					int, -- zip code
	unemployment		float, -- perc over 16yo
	poverty				float, -- per households
	income				float
)

-- taxi counts (start with just date)
-- 		we'll split it by type so that we can compare those. Seems interesting
CREATE TABLE IF NOT EXISTS(
	id					SERIAL PRIMARY KEY, -- primary key
	date				date, 
	zip					int,
	taxi_count			int,
	rideshare_count		int
)



-- database for output data
\c default -- connect to the "pg" admin database
SELECT 'CREATE DATABASE gold'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'gold')\gexec

\c gold;

