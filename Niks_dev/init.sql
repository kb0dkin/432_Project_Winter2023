
CREATE TABLE IF NOT EXISTS taxi_trips (
  company VARCHAR(255),
  dropoff_census_tract VARCHAR(255),
  dropoff_centroid_latitude NUMERIC(10, 7),
  dropoff_centroid_location POINT,
  dropoff_centroid_longitude NUMERIC(10, 7),
  dropoff_community_area INTEGER,
  extras NUMERIC(10, 2),
  fare NUMERIC(10, 2),
  payment_type VARCHAR(255),
  pickup_census_tract VARCHAR(255),
  pickup_centroid_latitude NUMERIC(10, 7),
  pickup_centroid_location POINT,
  pickup_centroid_longitude NUMERIC(10, 7),
  pickup_community_area INTEGER,
  taxi_id VARCHAR(255),
  tips NUMERIC(10, 2),
  tolls NUMERIC(10, 2),
  trip_end_timestamp TIMESTAMP,
  trip_id VARCHAR(255),
  trip_miles NUMERIC(10, 2),
  trip_seconds INTEGER,
  trip_start_timestamp TIMESTAMP,
  trip_total NUMERIC(10, 2)
);



