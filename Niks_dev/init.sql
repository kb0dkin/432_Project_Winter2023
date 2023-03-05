CREATE TABLE IF NOT EXISTS taxi_trips(
trip_id varchar(50) PRIMARY KEY, -- trip id hash
taxi_id varchar(128), -- taxi id hash
trip_seconds int, -- trip length in seconds
trip_miles float, -- not very useful, since this is really based off census tracts...
pickup_centroid_latitude float, -- latitude of pickup location
pickup_centroid_longitude float, -- longitude of pickup location
dropoff_centroid_latitude float, -- latitude of dropoff location
dropoff_centroid_longitude float, -- longitude of dropoff location
pickup_community_area int, -- community area number of the pickup location. Blank outside Chicago
dropoff_community_area int -- community area number of the dropoff location. Blank outside Chicago
);

-- COVID 19 Daily Cases

CREATE TABLE IF NOT EXISTS covid_19_daily_cases(
	lab_report_date		date PRIMARY KEY,
	cases_total			int,
	deaths_total			int,
	hospitalizations_total	int
	);

-- covid_19_zip	:	weekly covid incidence data by zip code
CREATE TABLE IF NOT EXISTS covid_19_zip(
	row_id      VARCHAR(15) PRIMARY KEY, -- auto incrementing primary key
	zip_code				varchar(8), -- zip code
	week_number		int, -- week number, beginning 2020. see CDC MMWR weeks
	week_start		date, -- beginning of the week
	cases_weekly		int,  -- empty if less than 5
	case_rate_cumulative		float,	-- weekly rate per 100k
	deaths_weekly		int, 	-- weekly deaths
	death_rate_weekly		float	-- deaths per 100k
    );

-- TNP_trips	:	list of rideshare trips, with start and end points
CREATE TABLE IF NOT EXISTS TNP_trips(
	trip_id				VARCHAR(50) PRIMARY KEY, -- trip id hash 
	trip_seconds			int,	-- trip length in seconds
	trip_miles			float,	-- not very useful, since this is really based off census tracts...
	pickup_community_area       int,	-- community area number. blank outside chicago
    dropoff_community_area		int,	-- community area number. blank outside chicago
	pickup_centroid_latitude	float,	-- latitude of pickup location
    pickup_centroid_longitude	float,	-- longitude of pickup location
    dropoff_centroid_latitude	float,	-- latitude of dropoff location
    dropoff_centroid_longitude	float	-- longitude of dropoff location
    );

-- build_permit	:	list of building permits
CREATE TABLE IF NOT EXISTS  build_permit(
	id			int PRIMARY KEY, -- building permit id
	permit_			int,  -- number assigned at beginning of application process
	application_start_date		date, -- start of application date
	issue_date			date, -- date it was issued
	community_area			int,  -- community area number
	ward				int,  -- I would argue this is more important that community area
	latitude			float, -- latitude of the building
	longitude			float -- longitude of the building
);
