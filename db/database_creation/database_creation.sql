
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


-- database for output data
\c default -- connect to the "pg" admin database
SELECT 'CREATE DATABASE gold'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'gold')\gexec

\c gold;

