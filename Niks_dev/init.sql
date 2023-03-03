-- taxi_trips	:	list of taxi trips, with start and end points
CREATE TABLE IF NOT EXISTS taxi_trips(
	trip_id				varchar(50) PRIMARY KEY, -- trip id hash 
	taxi_id				varchar(128), -- taxi id hash
	trip_seconds			int,	-- trip length in seconds
	trip_miles			float,	-- not very useful, since this is really based off census tracts...
	community_area_pickup		int,	-- community area number. blank outside chicago
	dropoff_community_area		int		-- community area number. blank outside chicago
)



